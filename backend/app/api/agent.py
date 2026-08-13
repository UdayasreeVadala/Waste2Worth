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
from app.schemas.event import TransactionEventResponse
from app.services.agent_service import run_agent_for_match
from app.services.ai_service import analyze_waste_listing
from app.services.auth_service import get_current_user

router = APIRouter()


class AgentContactRequest(BaseModel):
    waste_id: int
    buyer_id: int
    minimum_total_price: float
    requires_pickup: bool = True
    allow_counter_offer: bool = True


class AgentRetryRequest(BaseModel):
    minimum_total_price: float
    requires_pickup: bool = True
    allow_counter_offer: bool = True


@router.post("/contact")
def contact_buyer(
    request: AgentContactRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "supplier":
        raise HTTPException(status_code=403, detail="Only suppliers can contact buyers")

    waste = db.query(WasteListing).filter(WasteListing.id == request.waste_id).first()
    buyer = db.query(Buyer).filter(Buyer.id == request.buyer_id).first()

    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")
    if waste.supplier_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only contact buyers for your own waste")
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
    db.commit()
    db.refresh(match)
    db.refresh(transaction)

    waste.status = "matched"
    db.commit()

    agent_result = run_agent_for_match(
        db,
        match,
        transaction,
        buyer,
        waste,
        {
            "minimum_total_price": request.minimum_total_price,
            "requires_pickup": request.requires_pickup,
            "allow_counter_offer": request.allow_counter_offer,
        },
        supplier_approved=True,
    )

    if agent_result["status"] in {"deal_confirmed", "buyer_offer_accepted", "counter_offer_accepted"}:
        db.commit()

    return {
        "match": _match_payload(match),
        "transaction": _transaction_payload(transaction),
        "agent_result": agent_result,
        "events": _events_payload(db, transaction.id, match.id),
    }


@router.post("/matches/{match_id}/retry")
def retry_agent_contact(
    match_id: int,
    request: AgentRetryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "supplier":
        raise HTTPException(status_code=403, detail="Only suppliers can retry agent contact")

    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    waste = db.query(WasteListing).filter(WasteListing.id == match.waste_id).first()
    buyer = db.query(Buyer).filter(Buyer.id == match.buyer_id).first()
    if not waste or not buyer or waste.supplier_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    transaction = db.query(Transaction).filter(Transaction.match_id == match.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    agent_result = run_agent_for_match(
        db,
        match,
        transaction,
        buyer,
        waste,
        {
            "minimum_total_price": request.minimum_total_price,
            "requires_pickup": request.requires_pickup,
            "allow_counter_offer": request.allow_counter_offer,
        },
        supplier_approved=True,
    )

    return {
        "match": _match_payload(match),
        "transaction": _transaction_payload(transaction),
        "agent_result": agent_result,
        "events": _events_payload(db, transaction.id, match.id),
    }


@router.get("/activity")
def agent_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction_ids = [
        row.id
        for row in db.query(Transaction)
        .filter(
            (Transaction.supplier_id == current_user.id)
            | (Transaction.buyer_user_id == current_user.id)
        )
        .all()
    ]
    if not transaction_ids:
        return {"events": []}

    events = (
        db.query(TransactionEvent)
        .filter(TransactionEvent.transaction_id.in_(transaction_ids))
        .order_by(TransactionEvent.created_at.desc())
        .limit(100)
        .all()
    )
    return {"events": [TransactionEventResponse.model_validate(event).model_dump() for event in events]}


def _events_payload(db, transaction_id, match_id):
    events = (
        db.query(TransactionEvent)
        .filter(
            (TransactionEvent.transaction_id == transaction_id)
            | (TransactionEvent.match_id == match_id)
        )
        .order_by(TransactionEvent.created_at.asc())
        .all()
    )
    return [TransactionEventResponse.model_validate(event).model_dump() for event in events]


def _match_payload(match):
    return {
        "id": match.id,
        "waste_id": match.waste_id,
        "buyer_id": match.buyer_id,
        "buyer_name": match.buyer_name,
        "score": match.score,
        "explanation": match.explanation,
        "buyer_offer": match.buyer_offer,
        "transport_cost": match.transport_cost,
        "platform_fee": match.platform_fee,
        "supplier_earning": match.supplier_earning,
        "price_per_kg": match.price_per_kg,
        "currency": match.currency,
        "status": match.status,
    }


def _transaction_payload(transaction):
    return {
        "id": transaction.id,
        "match_id": transaction.match_id,
        "supplier_id": transaction.supplier_id,
        "buyer_user_id": transaction.buyer_user_id,
        "buyer_profile_id": transaction.buyer_profile_id,
        "waste_id": transaction.waste_id,
        "waste_type": transaction.waste_type,
        "quantity_kg": transaction.quantity_kg,
        "currency": transaction.currency,
        "final_price": transaction.final_price,
        "transport_cost": transaction.transport_cost,
        "platform_fee": transaction.platform_fee,
        "supplier_earning": transaction.supplier_earning,
        "pickup_method": transaction.pickup_method,
        "pickup_date": transaction.pickup_date,
        "status": transaction.status,
    }