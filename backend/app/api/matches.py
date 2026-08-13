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
from app.services.ai_service import analyze_waste_listing
from app.services.auth_service import get_current_user

router = APIRouter()


class StartMatchRequest(BaseModel):
    waste_id: int
    buyer_id: int


@router.post("/start")
def start_match(
    request: StartMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a match and transaction without running the AI agent (direct negotiation path)."""
    if current_user.role != "supplier":
        raise HTTPException(status_code=403, detail="Only suppliers can start matches")

    waste = db.query(WasteListing).filter(WasteListing.id == request.waste_id).first()
    buyer = db.query(Buyer).filter(Buyer.id == request.buyer_id).first()

    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")
    if waste.supplier_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    result = analyze_waste_listing(waste, [buyer])
    if result["best_buyer"] is None:
        raise HTTPException(status_code=400, detail="This buyer cannot handle the waste currently")

    selected = result["best_buyer"]
    margin = selected["estimated_margin"]

    match = Match(
        waste_id=waste.id,
        buyer_id=buyer.id,
        buyer_name=buyer.business_name,
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
        buyer_user_id=buyer.owner_id,
        buyer_profile_id=buyer.id,
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

    db.add(
        TransactionEvent(
            transaction_id=transaction.id,
            match_id=match.id,
            event_type="match_found",
            actor="supplier",
            message=f"Supplier selected {buyer.business_name} for {waste.produce_type}.",
        )
    )

    waste.status = "matched"
    db.commit()
    db.refresh(match)
    db.refresh(transaction)

    return {"match": _match_row(db, match), "transaction": {"id": transaction.id, "status": transaction.status}}


def _match_row(db, match):
    waste = db.query(WasteListing).filter(WasteListing.id == match.waste_id).first()
    buyer = db.query(Buyer).filter(Buyer.id == match.buyer_id).first()
    transaction = db.query(Transaction).filter(Transaction.match_id == match.id).first()
    return {
        "id": match.id,
        "waste_id": match.waste_id,
        "buyer_id": match.buyer_id,
        "buyer_name": match.buyer_name or (buyer.business_name if buyer else None),
        "buyer_type": buyer.buyer_type if buyer else None,
        "buyer_location": buyer.location if buyer else None,
        "waste": {
            "produce_type": waste.produce_type if waste else None,
            "quantity_kg": waste.quantity_kg if waste else None,
            "condition": waste.condition if waste else None,
            "location": waste.location if waste else None,
            "photo_url": waste.photo_url if waste else None,
            "status": waste.status if waste else None,
        },
        "score": match.score,
        "explanation": match.explanation,
        "buyer_offer": match.buyer_offer,
        "transport_cost": match.transport_cost,
        "platform_fee": match.platform_fee,
        "supplier_earning": match.supplier_earning,
        "price_per_kg": match.price_per_kg,
        "currency": match.currency,
        "status": match.status,
        "transaction_id": transaction.id if transaction else None,
        "created_at": str(match.created_at) if match.created_at else None,
    }


@router.get("/")
def my_matches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "supplier":
        waste_ids = [
            row[0]
            for row in db.query(WasteListing.id).filter(WasteListing.supplier_id == current_user.id).all()
        ]
        if not waste_ids:
            return {"matches": []}
        matches = (
            db.query(Match)
            .filter(Match.waste_id.in_(waste_ids))
            .order_by(Match.created_at.desc())
            .all()
        )
        return {"matches": [_match_row(db, match) for match in matches]}

    if current_user.role == "buyer":
        transaction_match_ids = [
            row[0]
            for row in db.query(Transaction.match_id)
            .filter(Transaction.buyer_user_id == current_user.id, Transaction.match_id.isnot(None))
            .all()
        ]
        if not transaction_match_ids:
            return {"matches": []}
        matches = (
            db.query(Match)
            .filter(Match.id.in_(transaction_match_ids))
            .order_by(Match.created_at.desc())
            .all()
        )
        return {"matches": [_match_row(db, match) for match in matches]}

    raise HTTPException(status_code=403, detail="Not allowed")