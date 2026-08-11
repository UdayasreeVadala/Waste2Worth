from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.waste import WasteListing
from app.models.buyer import Buyer
from app.models.match import Match
from app.schemas.match import MatchResponse
from app.services.ai_service import find_ai_ranked_buyers
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/{waste_id}", response_model=list[MatchResponse])
def get_matches_for_waste(
    waste_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    waste = db.query(WasteListing).filter(WasteListing.id == waste_id).first()

    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")

    if current_user.role != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can check matches")

    if waste.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only check your own waste listings")

    buyers = db.query(Buyer).all()

    return find_ai_ranked_buyers(waste, buyers)

@router.post("/{waste_id}/accept/{buyer_id}")
def accept_match(
    waste_id: int,
    buyer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    waste = db.query(WasteListing).filter(WasteListing.id == waste_id).first()
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()

    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")

    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    if current_user.role != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can accept matches")

    if waste.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only accept matches for your own waste")

    matches = find_ai_ranked_buyers(waste, [buyer])

    if not matches:
        raise HTTPException(status_code=400, detail="Buyer cannot handle this waste quantity")

    selected = matches[0]

    new_match = Match(
        waste_id=waste_id,
        buyer_id=buyer_id,
        transport_cost=selected["transport_cost"],
        farmer_earning=selected["farmer_earning"],
        status="accepted"
    )

    waste.status = "matched"

    db.add(new_match)
    db.commit()

    return {
        "message": "Match accepted successfully",
        "farmer_earning": selected["farmer_earning"],
        "transport_cost": selected["transport_cost"]
    }
