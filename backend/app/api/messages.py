from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.buyer import Buyer
from app.models.message import Message
from app.models.transaction import Transaction
from app.models.user import User
from app.models.waste import WasteListing
from app.schemas.message import MessageCreate, MessageResponse
from app.services.auth_service import get_current_user

router = APIRouter()


def _guard(db, transaction_id, user):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if transaction.supplier_id != user.id and transaction.buyer_user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not part of this conversation")
    return transaction


@router.get("/conversations")
def my_conversations(
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

    conversations = []
    for transaction in transactions:
        messages = (
            db.query(Message)
            .filter(Message.transaction_id == transaction.id)
            .order_by(Message.id.asc())
            .all()
        )
        buyer = db.query(Buyer).filter(Buyer.id == transaction.buyer_profile_id).first()
        supplier = db.query(User).filter(User.id == transaction.supplier_id).first()
        waste = db.query(WasteListing).filter(WasteListing.id == transaction.waste_id).first()

        conversations.append(
            {
                "transaction_id": transaction.id,
                "status": transaction.status,
                "waste_label": f"{waste.produce_type} ({transaction.quantity_kg} kg)" if waste else f"{transaction.waste_type}",
                "other_party": (
                    buyer.business_name if buyer and current_user.id == transaction.supplier_id
                    else (supplier.name if supplier else "Unknown")
                ),
                "message_count": len(messages),
                "last_message": messages[-1].content if messages else None,
                "last_message_sender_role": messages[-1].sender_role if messages else None,
            }
        )

    return {"conversations": conversations}


@router.get("/transactions/{transaction_id}/messages", response_model=list[MessageResponse])
def transaction_messages(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _guard(db, transaction_id, current_user)
    return (
        db.query(Message)
        .filter(Message.transaction_id == transaction_id)
        .order_by(Message.id.asc())
        .all()
    )


@router.post("/transactions/{transaction_id}/messages", response_model=MessageResponse)
def send_message(
    transaction_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _guard(db, transaction_id, current_user)

    new_message = Message(
        transaction_id=transaction_id,
        sender_id=current_user.id,
        sender_role=current_user.role,
        content=message.content,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message