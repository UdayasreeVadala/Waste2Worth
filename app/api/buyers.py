from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.buyer import Buyer
from app.schemas.buyer import BuyerCreate, BuyerResponse
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=BuyerResponse)
def create_buyer(
    buyer: BuyerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can create buyer profile")

    new_buyer = Buyer(
        owner_id=current_user.id,
        **buyer.model_dump()
    )

    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)

    return new_buyer

@router.get("/", response_model=list[BuyerResponse])
def get_buyers(db: Session = Depends(get_db)):
    return db.query(Buyer).all()

@router.get("/my-profile", response_model=list[BuyerResponse])
def get_my_buyer_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Buyer).filter(Buyer.owner_id == current_user.id).all()