from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.buyer import Buyer
from app.models.match import Match
from app.models.user import User
from app.models.waste import WasteListing
from app.schemas.agent import AgentContactRequest, AgentContactResponse
from app.services.ai_service import evaluate_waste_listing
from app.services.auth_service import get_current_user
from waste2worth_agent import Waste2WorthAgent

router = APIRouter()


@router.post("/matches/{match_id}/contact", response_model=AgentContactResponse)
def contact_buyer_for_match(
    match_id: int,
    request: AgentContactRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    waste = db.query(WasteListing).filter(WasteListing.id == match.waste_id).first()
    buyer = db.query(Buyer).filter(Buyer.id == match.buyer_id).first()
    if not waste or not buyer:
        raise HTTPException(status_code=404, detail="Match is missing waste or buyer details")

    if current_user.role != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can start agent contact")

    if waste.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only start contact for your own waste")

    ai_result = evaluate_waste_listing(waste, [buyer])
    if not ai_result["best_buyer"]:
        raise HTTPException(status_code=400, detail="Selected buyer is no longer suitable")

    agent = Waste2WorthAgent(
        communication_gateway=LocalBuyerCommunicationGateway(buyer, waste),
        transaction_gateway=MatchTransactionGateway(db, match),
        event_gateway=InMemoryEventGateway(),
    )

    result = agent.contact_and_negotiate(
        transaction_id=str(match.id),
        waste_analysis=ai_result["analysis"],
        selected_buyer=ai_result["best_buyer"],
        supplier_rules=request.model_dump(exclude={"supplier_approved_contact"}),
        supplier_approved_contact=request.supplier_approved_contact,
    )

    return result


class LocalBuyerCommunicationGateway:
    def __init__(self, buyer, waste):
        self.buyer = buyer
        self.waste = waste
        self.latest_counter_offer = None

    def send_waste_offer(self, buyer_id, payload):
        if "counter_offer" in payload:
            self.latest_counter_offer = payload["counter_offer"]
            return self.latest_counter_offer

        return f"conversation_match_buyer_{buyer_id}"

    def get_buyer_response(self, conversation_id):
        return {
            "total_price": round(self.waste.quantity_kg * self.buyer.price_per_kg, 2),
            "pickup_included": bool(getattr(self.buyer, "pickup_available", True)),
        }


class MatchTransactionGateway:
    def __init__(self, db, match):
        self.db = db
        self.match = match

    def update_transaction_status(self, transaction_id, status, payload):
        self.match.status = status
        if payload.get("final_total_price") is not None:
            self.match.farmer_earning = payload["final_total_price"]
        self.db.commit()


class InMemoryEventGateway:
    def __init__(self):
        self.events = []

    def record_event(self, transaction_id, event_type, actor, message, payload=None):
        self.events.append(
            {
                "transaction_id": transaction_id,
                "event_type": event_type,
                "actor": actor,
                "message": message,
                "payload": payload or {},
            }
        )

