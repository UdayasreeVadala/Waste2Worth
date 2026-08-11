from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.waste import WasteListing
from app.schemas.waste import WasteCreate, WasteResponse
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=WasteResponse)
def create_waste_listing(
    waste: WasteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can upload waste")

    new_waste = WasteListing(
        farmer_id=current_user.id,
        **waste.model_dump()
    )

    db.add(new_waste)
    db.commit()
    db.refresh(new_waste)

    return new_waste

@router.get("/", response_model=list[WasteResponse])
def get_waste_listings(db: Session = Depends(get_db)):
    return db.query(WasteListing).all()

@router.get("/my-listings", response_model=list[WasteResponse])
def get_my_waste_listings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WasteListing).filter(
        WasteListing.farmer_id == current_user.id
    ).all()