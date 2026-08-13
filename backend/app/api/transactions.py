from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.buyer import Buyer
from app.models.event import TransactionEvent
from app.models.match import Match
from app.models.transaction import Transaction
from app.models.user import User
from app.models.waste import WasteListing
from app.schemas.transaction import BuyerRespondRequest, SchedulePickupRequest
from app.services.auth_service import get_current_user

router = APIRouter()

ACTIVE_STATUSES = {"match_found", "buyer_contacted", "offer_received", "deal_confirmed", "pickup_scheduled", "collected"}


def _get_transaction_or_404(db, transaction_id):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


def _guard_access(user, transaction):
    if transaction.supplier_id != user.id and transaction.buyer_user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not part of this transaction")
    return user.id == transaction.supplier_id


def _record_event(db, transaction, event_type, actor, message, payload=None):
    db.add(
        TransactionEvent(
            transaction_id=transaction.id,
            match_id=transaction.match_id,
            event_type=event_type,
            actor=actor,
            message=message,
            payload=payload or {},
        )
    )


def _compose_detail(db, transaction):
    buyer_profile = db.query(Buyer).filter(Buyer.id == transaction.buyer_profile_id).first()
    supplier = db.query(User).filter(User.id == transaction.supplier_id).first()
    buyer_user = db.query(User).filter(User.id == transaction.buyer_user_id).first()
    waste = db.query(WasteListing).filter(WasteListing.id == transaction.waste_id).first()
    match = db.query(Match).filter(Match.id == transaction.match_id).first()
    events = (
        db.query(TransactionEvent)
        .filter(TransactionEvent.transaction_id == transaction.id)
        .order_by(TransactionEvent.created_at.asc())
        .all()
    )

    return {
        "id": transaction.id,
        "match_id": transaction.match_id,
        "supplier_id": transaction.supplier_id,
        "supplier_name": supplier.name if supplier else None,
        "buyer_user_id": transaction.buyer_user_id,
        "buyer_business_name": (buyer_profile.business_name if buyer_profile else (buyer_user.name if buyer_user else None)),
        "buyer_profile_id": transaction.buyer_profile_id,
        "waste_id": transaction.waste_id,
        "waste": {
            "id": waste.id if waste else None,
            "produce_type": waste.produce_type if waste else transaction.waste_type,
            "quantity_kg": transaction.quantity_kg,
            "condition": waste.condition if waste else None,
            "location": waste.location if waste else None,
            "photo_url": waste.photo_url if waste else None,
        },
        "currency": transaction.currency,
        "final_price": transaction.final_price,
        "transport_cost": transaction.transport_cost,
        "platform_fee": transaction.platform_fee,
        "supplier_earning": transaction.supplier_earning,
        "pickup_method": transaction.pickup_method,
        "pickup_date": transaction.pickup_date,
        "status": transaction.status,
        "match": {
            "id": match.id if match else None,
            "buyer_name": match.buyer_name if match else None,
            "score": match.score if match else None,
            "explanation": match.explanation if match else None,
        },
        "created_at": str(transaction.created_at) if transaction.created_at else None,
        "events": [
            {
                "id": event.id,
                "event_type": event.event_type,
                "actor": event.actor,
                "message": event.message,
                "payload": event.payload or {},
            }
            for event in events
        ],
    }


@router.get("/my")
def my_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transactions = (
        db.query(Transaction)
        .filter(
            (Transaction.supplier_id == current_user.id)
            | (Transaction.buyer_user_id == current_user.id)
        )
        .order_by(Transaction.created_at.desc())
        .all()
    )
    return {"transactions": [_compose_detail(db, transaction) for transaction in transactions]}


@router.get("/{transaction_id}")
def transaction_detail(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = _get_transaction_or_404(db, transaction_id)
    _guard_access(user=current_user, transaction=transaction)
    return _compose_detail(db, transaction)


@router.post("/{transaction_id}/respond")
def buyer_respond(
    transaction_id: int,
    request: BuyerRespondRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = _get_transaction_or_404(db, transaction_id)

    if current_user.id != transaction.buyer_user_id:
        raise HTTPException(status_code=403, detail="Only the buyer can respond to this transaction")
    if transaction.status not in {"match_found", "buyer_contacted", "offer_received"}:
        raise HTTPException(status_code=400, detail=f"Cannot respond when status is {transaction.status}")

    action = request.action.lower()
    if action == "accept":
        transaction.status = "deal_confirmed"
        transaction.final_price = transaction.final_price or transaction.supplier_earning
        _record_event(db, transaction, "deal_confirmed", "buyer", "Buyer accepted the deal.")
    elif action == "reject":
        transaction.status = "offer_rejected"
        _record_event(db, transaction, "offer_rejected", "buyer", "Buyer rejected the deal.")
    elif action == "offer":
        if request.price is None:
            raise HTTPException(status_code=400, detail="price is required for an offer")
        transaction.final_price = request.price
        transaction.supplier_earning = request.price
        transaction.status = "offer_received"
        _record_event(
            db,
            transaction,
            "counter_offer_sent",
            "buyer",
            "Buyer made a counter offer.",
            {"price": request.price, "pickup_included": request.pickup_included},
        )
    else:
        raise HTTPException(status_code=400, detail="action must be accept, reject or offer")

    match = db.query(Match).filter(Match.id == transaction.match_id).first()
    if match:
        match.status = transaction.status

    db.commit()
    return _compose_detail(db, transaction)


@router.post("/{transaction_id}/accept-offer")
def supplier_accept_offer(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = _get_transaction_or_404(db, transaction_id)
    is_supplier = _guard_access(user=current_user, transaction=transaction)
    if not is_supplier:
        raise HTTPException(status_code=403, detail="Only the supplier can accept the buyer offer")
    if transaction.status != "offer_received":
        raise HTTPException(status_code=400, detail="There is no open buyer offer to accept")

    transaction.status = "deal_confirmed"
    transaction.supplier_earning = transaction.final_price
    _record_event(db, transaction, "deal_confirmed", "supplier", "Supplier accepted the buyer offer.")

    match = db.query(Match).filter(Match.id == transaction.match_id).first()
    if match:
        match.status = "deal_confirmed"
        match.supplier_earning = transaction.final_price

    db.commit()
    return _compose_detail(db, transaction)


@router.post("/{transaction_id}/schedule-pickup")
def schedule_pickup(
    transaction_id: int,
    request: SchedulePickupRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = _get_transaction_or_404(db, transaction_id)
    _guard_access(user=current_user, transaction=transaction)
    if transaction.status not in {"deal_confirmed", "pickup_scheduled"}:
        raise HTTPException(status_code=400, detail=f"Cannot schedule pickup when status is {transaction.status}")

    transaction.pickup_method = request.pickup_method
    transaction.pickup_date = request.pickup_date
    transaction.status = "pickup_scheduled"
    _record_event(
        db,
        transaction,
        "pickup_scheduled",
        "system",
        "Pickup scheduled.",
        {"method": request.pickup_method, "date": request.pickup_date},
    )

    match = db.query(Match).filter(Match.id == transaction.match_id).first()
    if match:
        match.status = "pickup_scheduled"

    db.commit()
    return _compose_detail(db, transaction)


@router.post("/{transaction_id}/confirm-collected")
def confirm_collected(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = _get_transaction_or_404(db, transaction_id)
    _guard_access(user=current_user, transaction=transaction)
    if transaction.status != "pickup_scheduled":
        raise HTTPException(status_code=400, detail=f"Cannot confirm collection when status is {transaction.status}")

    transaction.status = "collected"
    _record_event(db, transaction, "collected", "supplier", "Waste collected by buyer.")

    match = db.query(Match).filter(Match.id == transaction.match_id).first()
    if match:
        match.status = "collected"

    db.commit()
    return _compose_detail(db, transaction)


@router.post("/{transaction_id}/complete")
def complete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = _get_transaction_or_404(db, transaction_id)
    _guard_access(user=current_user, transaction=transaction)
    if transaction.status not in {"collected", "pickup_scheduled", "deal_confirmed"}:
        raise HTTPException(status_code=400, detail=f"Cannot complete transaction when status is {transaction.status}")

    transaction.status = "completed"
    _record_event(db, transaction, "completed", "system", "Transaction completed.")

    match = db.query(Match).filter(Match.id == transaction.match_id).first()
    if match:
        match.status = "completed"

    waste = db.query(WasteListing).filter(WasteListing.id == transaction.waste_id).first()
    if waste:
        waste.status = "completed"

    db.commit()
    return _compose_detail(db, transaction)


@router.post("/{transaction_id}/cancel")
def cancel_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = _get_transaction_or_404(db, transaction_id)
    _guard_access(user=current_user, transaction=transaction)
    if transaction.status in {"completed", "offer_rejected", "cancelled"}:
        raise HTTPException(status_code=400, detail=f"Cannot cancel transaction with status {transaction.status}")

    transaction.status = "cancelled"
    _record_event(db, transaction, "cancelled", "system", "Transaction cancelled.")

    match = db.query(Match).filter(Match.id == transaction.match_id).first()
    if match:
        match.status = "cancelled"

    waste = db.query(WasteListing).filter(WasteListing.id == transaction.waste_id).first()
    if waste and waste.status == "matched":
        waste.status = "available"

    db.commit()
    return _compose_detail(db, transaction)