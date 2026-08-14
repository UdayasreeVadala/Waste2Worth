import os

os.environ["WASTE2WORTH_USE_AI"] = "0"

from waste2worth_agent.messaging import generate_outreach_message, suggest_counter_offer


ANALYSIS = {
    "display_name": "Tomato waste",
    "waste_type": "tomato",
    "quantity_kg": 700,
    "condition": "spoiled",
}

BUYER = {
    "buyer_id": "buyer_1",
    "name": "GreenBio Energy",
    "business_type": "Biogas plant",
    "location": {"address": "Nashik Industrial Area", "city": "Nashik", "country": "India"},
}


def test_outreach_template_contains_key_facts():
    message = generate_outreach_message(ANALYSIS, BUYER, {"minimum_total_price": 180, "requires_pickup": True})
    assert message["source"] == "template"
    assert "Tomato waste" in message["subject"]
    assert "700" in message["subject"]
    assert "GreenBio Energy" in message["body"]
    assert "180" in message["body"]


def test_counter_offer_floor_enforced():
    counter = suggest_counter_offer(
        ANALYSIS,
        BUYER,
        {"minimum_total_price": 500, "requires_pickup": True},
        latest_offer={"total_price": 100, "pickup_included": False},
    )
    assert counter["total_price"] >= 500
    assert counter["source"] == "rule_negotiation"


def test_counter_offer_zero_floor():
    counter = suggest_counter_offer(ANALYSIS, BUYER, {"minimum_total_price": 0, "requires_pickup": False})
    assert counter["total_price"] == 0
    assert counter["pickup_included"] is False
