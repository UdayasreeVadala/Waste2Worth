from app.models.event import TransactionEvent
from waste2worth_agent import Waste2WorthAgent

STATUS_MAP = {
    "waiting_for_supplier_approval": "match_found",
    "buyer_contacted": "buyer_contacted",
    "offer_received": "offer_received",
    "counter_offer_sent": "offer_received",
    "buyer_offer_accepted": "deal_confirmed",
    "counter_offer_accepted": "deal_confirmed",
    "deal_confirmed": "deal_confirmed",
    "offer_rejected": "offer_rejected",
}


class BuyerSimulationGateway:
    """Simulates the buyer's channel. In production this becomes email/WhatsApp/in-app messaging."""

    def __init__(self, buyer, waste):
        self.buyer = buyer
        self.waste = waste
        self.latest_counter_offer = None

    def send_waste_offer(self, buyer_id, payload):
        if "counter_offer" in payload:
            self.latest_counter_offer = payload["counter_offer"]
            return self.latest_counter_offer
        return f"conversation_buyer_{buyer_id}"

    def get_buyer_response(self, conversation_id):
        return {
            "total_price": round(self.waste.quantity_kg * self.buyer.price_per_kg, 2),
            "pickup_included": bool(getattr(self.buyer, "pickup_available", True)),
        }


class DatabaseTransactionGateway:
    def __init__(self, db, transaction, match):
        self.db = db
        self.transaction = transaction
        self.match = match

    def update_transaction_status(self, transaction_id, status, payload=None):
        payload = payload or {}
        friendly = STATUS_MAP.get(status, status)

        if payload.get("final_total_price") is not None:
            self.transaction.final_price = payload["final_total_price"]
            self.transaction.supplier_earning = payload["final_total_price"]
            self.match.supplier_earning = payload["final_total_price"]
            self.match.buyer_offer = payload["final_total_price"]

        if payload.get("pickup_included") is not None:
            self.transaction.pickup_method = (
                "buyer_pickup" if payload["pickup_included"] else "supplier_delivery"
            )
            self.match.transport_cost = (
                0.0 if payload["pickup_included"] else (self.transaction.quantity_kg or 0) * 1.4
            )

        self.transaction.status = friendly
        self.match.status = friendly
        self.db.commit()


class DatabaseEventGateway:
    def __init__(self, db, transaction=None, match=None):
        self.db = db
        self.transaction = transaction
        self.match = match

    def record_event(self, transaction_id, event_type, actor, message, payload=None):
        row = TransactionEvent(
            transaction_id=self.transaction.id if self.transaction else None,
            match_id=self.match.id if self.match else None,
            event_type=event_type,
            actor=actor,
            message=message,
            payload=payload or {},
        )
        self.db.add(row)
        self.db.commit()


def run_agent_for_match(db, match, transaction, buyer, waste, rules, supplier_approved=True):
    from app.services.ai_service import analyze_waste_listing

    ai_result = analyze_waste_listing(waste, [buyer])
    if ai_result["best_buyer"] is None:
        match.status = "offer_rejected"
        transaction.status = "offer_rejected"
        db.commit()
        return {
            "status": "offer_rejected",
            "events": [],
            "deal": None,
        }

    selected_buyer = ai_result["best_buyer"]
    agent = Waste2WorthAgent(
        communication_gateway=BuyerSimulationGateway(buyer, waste),
        transaction_gateway=DatabaseTransactionGateway(db, transaction, match),
        event_gateway=DatabaseEventGateway(db, transaction, match),
    )

    result = agent.contact_and_negotiate(
        transaction_id=str(transaction.id),
        waste_analysis=ai_result["analysis"],
        selected_buyer=selected_buyer,
        supplier_rules=rules,
        supplier_approved_contact=supplier_approved,
    )

    if result["deal"]:
        match.buyer_name = selected_buyer["name"]
        match.buyer_offer = result["deal"].get("final_total_price")
        match.currency = selected_buyer.get("currency") or "INR"
        transaction.final_price = result["deal"].get("final_total_price")
        transaction.supplier_earning = result["deal"].get("final_total_price")
        db.commit()

    return result