from waste2worth_agent.workflow import Waste2WorthAgent


class RecordingCommunicationGateway:
    def __init__(self, response=None):
        self.sent = []
        self.response = response or {"total_price": 210, "pickup_included": True}

    def send_waste_offer(self, buyer_id, payload):
        self.sent.append((buyer_id, payload))
        if "counter_offer" in payload:
            return payload["counter_offer"]
        return "conversation_1"

    def get_buyer_response(self, conversation_id):
        return self.response


class RecordingTransactionGateway:
    def __init__(self):
        self.updates = []

    def update_transaction_status(self, transaction_id, status, payload):
        self.updates.append((transaction_id, status, payload))


class RecordingEventGateway:
    def __init__(self):
        self.events = []

    def record_event(self, transaction_id, event_type, actor, message, payload=None):
        self.events.append((transaction_id, event_type, actor, message, payload))


def test_agent_requires_supplier_approval():
    agent = Waste2WorthAgent(RecordingCommunicationGateway(), RecordingTransactionGateway())
    result = agent.contact_and_negotiate(
        transaction_id="txn_1",
        waste_analysis={"display_name": "Tomato waste", "quantity_kg": 700, "condition": "spoiled"},
        selected_buyer={"buyer_id": "buyer_1", "name": "GreenBio"},
        supplier_rules={"minimum_total_price": 180, "requires_pickup": True},
        supplier_approved_contact=False,
    )

    assert result["status"] == "waiting_for_supplier_approval"


def test_agent_confirms_acceptable_offer():
    tx_gateway = RecordingTransactionGateway()
    agent = Waste2WorthAgent(RecordingCommunicationGateway(), tx_gateway)
    result = agent.contact_and_negotiate(
        transaction_id="txn_1",
        waste_analysis={"display_name": "Tomato waste", "quantity_kg": 700, "condition": "spoiled"},
        selected_buyer={"buyer_id": "buyer_1", "name": "GreenBio"},
        supplier_rules={"minimum_total_price": 180, "requires_pickup": True},
        supplier_approved_contact=True,
    )

    assert result["status"] == "deal_confirmed"
    assert tx_gateway.updates[0][1] == "deal_confirmed"


def test_agent_rejects_offer_when_counter_not_allowed():
    tx_gateway = RecordingTransactionGateway()
    communication = RecordingCommunicationGateway(response={"total_price": 100, "pickup_included": False})
    agent = Waste2WorthAgent(communication, tx_gateway)
    result = agent.contact_and_negotiate(
        transaction_id="txn_1",
        waste_analysis={"display_name": "Tomato waste", "quantity_kg": 700, "condition": "spoiled"},
        selected_buyer={"buyer_id": "buyer_1", "name": "GreenBio"},
        supplier_rules={
            "minimum_total_price": 180,
            "requires_pickup": True,
            "allow_counter_offer": False,
        },
        supplier_approved_contact=True,
    )

    assert result["status"] == "offer_rejected"
    assert tx_gateway.updates[0][1] == "offer_rejected"


def test_agent_records_events_when_gateway_is_available():
    event_gateway = RecordingEventGateway()
    agent = Waste2WorthAgent(
        RecordingCommunicationGateway(),
        RecordingTransactionGateway(),
        event_gateway=event_gateway,
    )
    agent.contact_and_negotiate(
        transaction_id="txn_1",
        waste_analysis={"display_name": "Tomato waste", "quantity_kg": 700, "condition": "spoiled"},
        selected_buyer={"buyer_id": "buyer_1", "name": "GreenBio"},
        supplier_rules={"minimum_total_price": 180, "requires_pickup": True},
        supplier_approved_contact=True,
    )

    event_types = [event[1] for event in event_gateway.events]
    assert "buyer_contacted" in event_types
    assert "deal_confirmed" in event_types
