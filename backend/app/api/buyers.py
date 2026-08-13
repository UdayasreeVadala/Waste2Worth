from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.buyer import Buyer
from app.models.event import TransactionEvent
from app.models.match import Match
from app.models.transaction import Transaction
from app.models.user import User
from app.models.waste import WasteListing
from app.schemas.buyer import BuyerCreate, BuyerResponse, BuyerUpdate
from waste2worth_ai.errors import ContractError
from app.services.ai_service import analyze_waste_listing, evaluate_for_buyer
from app.services.auth_service import get_current_user

router = APIRouter()


class ExpressInterestRequest(BaseModel):
    waste_id: int
    profile_id: int | None = None


@router.post("/", response_model=BuyerResponse)
def create_buyer_profile(
    buyer: BuyerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can create buyer profiles")

    new_buyer = Buyer(owner_id=current_user.id, **buyer.model_dump())
    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)
    return new_buyer


@router.get("/my-profile", response_model=list[BuyerResponse])
def get_my_buyer_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Buyer).filter(Buyer.owner_id == current_user.id).all()


@router.put("/{buyer_id}", response_model=BuyerResponse)
def update_buyer_profile(
    buyer_id: int,
    updates: BuyerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer profile not found")
    if buyer.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own buyer profiles")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(buyer, field, value)

    db.commit()
    db.refresh(buyer)
    return buyer


@router.get("/recommended")
def get_recommended_waste(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """AI recommendations for the buyer: which available listings fit this buyer's profile."""
    if current_user.role != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can view recommended waste")

    profiles = db.query(Buyer).filter(Buyer.owner_id == current_user.id).all()
    if not profiles:
        return {"message": "Create a buyer profile first to receive recommendations", "listings": []}

    listings = (
        db.query(WasteListing)
        .filter(WasteListing.status == "available")
        .order_by(WasteListing.created_at.desc())
        .all()
    )

    recommendations = []
    for listing in listings:
        for profile in profiles:
            match = evaluate_for_buyer(listing, profile)
            if match is None:
                continue
            recommendations.append(
                {
                    "waste": _waste_dict(listing),
                    "match": {
                        "buyer_id": profile.id,
                        "distance_km": match["distance_km"],
                        "margin": match["estimated_margin"],
                        "explanation": match["explanation"],
                    },
                }
            )
            break

    recommendations.sort(key=lambda item: item["match"]["margin"]["estimated_supplier_earnings"], reverse=True)
    return {"listings": recommendations}


@router.post("/express-interest")
def express_interest(
    request: ExpressInterestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Buyer expresses interest in a waste listing -> creates a match + transaction."""
    if current_user.role != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can express interest")

    waste = db.query(WasteListing).filter(WasteListing.id == request.waste_id).first()
    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")
    if waste.status not in ("available", "matched"):
        raise HTTPException(status_code=400, detail="This waste is not currently available")

    profile = None
    if request.profile_id:
        profile = (
            db.query(Buyer)
            .filter(Buyer.id == request.profile_id, Buyer.owner_id == current_user.id)
            .first()
        )
    if not profile:
        profile = db.query(Buyer).filter(Buyer.owner_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Create a buyer profile first")

    try:
        result = analyze_waste_listing(waste, [profile])
    except ContractError as exc:
        raise HTTPException(status_code=400, detail=f"Could not analyze match: {exc.message}")
    if result["best_buyer"] is None:
        raise HTTPException(status_code=400, detail="Your profile cannot handle this waste currently")

    selected = result["best_buyer"]
    margin = selected["estimated_margin"]

    match = Match(
        waste_id=waste.id,
        buyer_id=profile.id,
        buyer_name=profile.business_name,
        score=selected["score"],
        explanation=selected["explanation"],
        buyer_offer=margin["buyer_offer"],
        transport_cost=margin["transport_cost"],
        platform_fee=margin["platform_fee"],
        supplier_earning=margin["estimated_supplier_earnings"],
        price_per_kg=selected["price_per_kg"],
        currency=selected.get("currency") or "INR",
        status="match_found",
    )
    db.add(match)
    db.flush()

    transaction = Transaction(
        match_id=match.id,
        supplier_id=waste.supplier_id,
        buyer_user_id=current_user.id,
        buyer_profile_id=profile.id,
        waste_id=waste.id,
        waste_type=waste.produce_type,
        quantity_kg=waste.quantity_kg,
        currency=selected.get("currency") or "INR",
        final_price=margin["buyer_offer"],
        transport_cost=margin["transport_cost"],
        platform_fee=margin["platform_fee"],
        supplier_earning=margin["estimated_supplier_earnings"],
        status="match_found",
    )
    db.add(transaction)
    db.flush()

    db.add(
        TransactionEvent(
            transaction_id=transaction.id,
            match_id=match.id,
            event_type="match_found",
            actor="buyer",
            message=f"{profile.business_name} expressed interest in {waste.produce_type}.",
        )
    )

    waste.status = "matched"
    db.commit()
    db.refresh(match)
    db.refresh(transaction)

    return {
        "match": {
            "id": match.id,
            "waste_id": match.waste_id,
            "buyer_id": match.buyer_id,
            "buyer_name": match.buyer_name,
            "score": match.score,
            "status": match.status,
        },
        "transaction": {"id": transaction.id, "status": transaction.status},
    }


def _waste_dict(listing):
    return {
        "id": listing.id,
        "produce_type": listing.produce_type,
        "quantity_kg": listing.quantity_kg,
        "condition": listing.condition,
        "location": listing.location,
        "notes": listing.notes,
        "photo_url": listing.photo_url,
        "available_from": listing.available_from,
        "available_until": listing.available_until,
        "status": listing.status,
    }