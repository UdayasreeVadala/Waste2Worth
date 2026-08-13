import streamlit as st

from waste2worth_agent.workflow import Waste2WorthAgent
from waste2worth_ai.pipeline import evaluate_waste_opportunity


st.set_page_config(
    page_title="Waste2Worth",
    page_icon="♻️",
    layout="wide",
)


BUYERS = [
    {
        "id": "1",
        "name": "GreenBio Energy",
        "business_type": "Biogas plant",
        "location": {
            "address": "Nashik Industrial Area",
            "latitude": 20.01,
            "longitude": 73.79,
        },
        "accepted_waste": ["tomato", "vegetable", "fruit", "food", "organic"],
        "min_quantity_kg": 100,
        "max_quantity_kg": 3000,
        "current_capacity_kg": 1500,
        "price_per_kg": 30,
        "currency": "INR",
        "pickup_available": True,
        "service_radius_km": 50,
        "availability_status": "available",
    },
    {
        "id": "2",
        "name": "EcoCompost Nashik",
        "business_type": "Composting company",
        "location": {
            "address": "Nashik Market Road",
            "latitude": 20.06,
            "longitude": 73.82,
        },
        "accepted_waste": ["tomato", "vegetable", "fruit", "food", "organic"],
        "min_quantity_kg": 50,
        "max_quantity_kg": 2000,
        "current_capacity_kg": 900,
        "price_per_kg": 27,
        "currency": "INR",
        "pickup_available": False,
        "service_radius_km": 40,
        "availability_status": "available",
    },
    {
        "id": "3",
        "name": "BioCycle Organics",
        "business_type": "Organic processor",
        "location": {
            "address": "Sinnar Road",
            "latitude": 19.85,
            "longitude": 73.99,
        },
        "accepted_waste": ["vegetable", "fruit", "food", "organic"],
        "min_quantity_kg": 200,
        "max_quantity_kg": 5000,
        "current_capacity_kg": 2200,
        "price_per_kg": 29,
        "currency": "INR",
        "pickup_available": True,
        "service_radius_km": 70,
        "availability_status": "limited",
    },
]


class DemoCommunicationGateway:
    def __init__(self, offer):
        self.offer = offer

    def send_waste_offer(self, buyer_id, payload):
        if "counter_offer" in payload:
            return payload["counter_offer"]
        return f"conversation_{buyer_id}"

    def get_buyer_response(self, conversation_id):
        return self.offer


class DemoTransactionGateway:
    def __init__(self):
        self.status_updates = []

    def update_transaction_status(self, transaction_id, status, payload):
        self.status_updates.append(
            {
                "transaction_id": transaction_id,
                "status": status,
                "payload": payload,
            }
        )


class DemoEventGateway:
    def __init__(self):
        self.events = []

    def record_event(self, transaction_id, event_type, actor, message, payload=None):
        self.events.append(
            {
                "event_type": event_type,
                "actor": actor,
                "message": message,
                "payload": payload or {},
            }
        )


def run_agent(ai_result, selected_buyer, minimum_price, requires_pickup):
    offer = {
        "total_price": selected_buyer["estimated_margin"]["buyer_offer"],
        "pickup_included": selected_buyer["pickup_available"],
    }
    transaction_gateway = DemoTransactionGateway()
    event_gateway = DemoEventGateway()
    agent = Waste2WorthAgent(
        communication_gateway=DemoCommunicationGateway(offer),
        transaction_gateway=transaction_gateway,
        event_gateway=event_gateway,
    )

    return agent.contact_and_negotiate(
        transaction_id="demo_txn_001",
        waste_analysis=ai_result["analysis"],
        selected_buyer=selected_buyer,
        supplier_rules={
            "minimum_total_price": minimum_price,
            "requires_pickup": requires_pickup,
            "allow_counter_offer": True,
        },
        supplier_approved_contact=True,
    )


st.title("Waste2Worth")
st.caption("AI-powered organic waste recovery marketplace")

with st.sidebar:
    st.header("Supplier Waste")
    waste_type = st.selectbox("Waste type", ["tomato", "vegetable", "fruit", "food", "organic"])
    quantity_kg = st.number_input("Quantity (kg)", min_value=1, value=700, step=50)
    condition = st.selectbox("Condition", ["spoiled", "fresh", "mixed", "unknown"])
    location = st.text_input("Location", value="Nashik")
    minimum_price = st.number_input("Minimum acceptable total price", min_value=0, value=18000, step=500)
    requires_pickup = st.checkbox("Pickup required", value=True)

waste_input = {
    "supplier_id": "demo_supplier",
    "waste_type": waste_type,
    "quantity_kg": quantity_kg,
    "condition": condition,
    "location": {
        "address": location,
        "latitude": 19.9975,
        "longitude": 73.7898,
    },
}

ai_result = evaluate_waste_opportunity(waste_input=waste_input, buyers=BUYERS)

metric_cols = st.columns(4)
metric_cols[0].metric("Waste listed", f"{quantity_kg:,.0f} kg")
metric_cols[1].metric("Possible buyers", len(ai_result["ranked_buyers"]))
metric_cols[2].metric("Recommended route", ai_result["recommended_use"]["recommended_label"])
metric_cols[3].metric("Agent status", ai_result["agent_status"].replace("_", " ").title())

left, right = st.columns([1, 1])

with left:
    st.subheader("AI Waste Analysis")
    st.write(ai_result["analysis"]["display_name"])
    st.write("Category:", ai_result["analysis"]["category"])
    st.write("Properties:", ", ".join(ai_result["analysis"]["properties"]))
    if ai_result["analysis"]["limitations"]:
        st.warning(" ".join(ai_result["analysis"]["limitations"]))

    st.subheader("Best Use Recommendation")
    st.success(ai_result["recommended_use"]["recommended_label"])
    st.write(ai_result["recommended_use"]["reason"])

with right:
    st.subheader("Ranked Buyers")
    if not ai_result["ranked_buyers"]:
        st.error(ai_result["error"]["message"])
    else:
        for index, buyer in enumerate(ai_result["ranked_buyers"], start=1):
            margin = buyer["estimated_margin"]
            with st.container(border=True):
                st.markdown(f"**#{index} {buyer['name']}**")
                st.write(buyer["business_type"])
                st.write(
                    f"Distance: {buyer['distance_km']} km | "
                    f"Pickup: {'Yes' if buyer['pickup_available'] else 'No'}"
                )
                st.write(
                    f"Buyer offer: {margin['currency']} {margin['buyer_offer']:,.2f} | "
                    f"Estimated supplier earning: {margin['currency']} "
                    f"{margin['estimated_supplier_earnings']:,.2f}"
                )
                st.caption(buyer["explanation"])

st.divider()
st.subheader("AI Agent")

if ai_result["best_buyer"] is None:
    st.info("No buyer is available for agent contact yet.")
elif st.button("Contact recommended buyer"):
    agent_result = run_agent(
        ai_result=ai_result,
        selected_buyer=ai_result["best_buyer"],
        minimum_price=minimum_price,
        requires_pickup=requires_pickup,
    )
    st.success(agent_result["status"].replace("_", " ").title())
    st.write("Agent events:")
    for event in agent_result["events"]:
        st.write(f"- {event}")
    if agent_result["deal"]:
        st.json(agent_result["deal"])
else:
    st.info("Supplier approval is required before the agent contacts a buyer.")

