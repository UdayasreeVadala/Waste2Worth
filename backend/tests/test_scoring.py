from waste2worth_ai.matcher import rank_buyers
from waste2worth_ai.scoring_config import SCORING
from waste2worth_ai.validation import parse_buyer


def _analysis():
    return {
        "waste_type": "tomato",
        "display_name": "Tomato waste",
        "quantity_kg": 700,
        "condition": "spoiled",
        "category": "Organic waste",
    }


def _buyer(**overrides):
    buyer = {
        "id": "buyer_1",
        "name": "GreenBio Energy",
        "business_type": "Biogas plant",
        "location": {"latitude": 19.9975, "longitude": 73.7898},
        "distance_km": 25,
        "service_radius_km": 50,
        "accepted_waste": ["tomato", "vegetable"],
        "min_quantity_kg": 100,
        "max_quantity_kg": 3000,
        "current_capacity_kg": 1500,
        "price_per_kg": 0.3,
        "currency": "USD",
        "pickup_available": True,
        "availability_status": "available",
    }
    buyer.update(overrides)
    return buyer


def _ranked(*buyers):
    return rank_buyers(_analysis(), [parse_buyer(buyer) for buyer in buyers])


def test_ranked_buyers_have_factor_breakdown():
    ranked = _ranked(_buyer())
    assert len(ranked) == 1
    row = ranked[0]
    breakdown = row["factor_breakdown"]
    assert breakdown["version"] == SCORING["version"]
    assert set(breakdown) >= {"earnings_points", "distance_points", "pickup_points", "capacity_points", "availability_points"}
    assert breakdown["pickup_points"] == SCORING["pickup_bonus"]


def test_pickup_bonus_and_breakdown_consistent():
    with_pickup = _ranked(_buyer())[0]
    without_pickup = _ranked(_buyer(pickup_available=False))[0]
    assert (
        with_pickup["factor_breakdown"]["pickup_points"]
        > without_pickup["factor_breakdown"]["pickup_points"]
    )
    assert with_pickup["score"] > without_pickup["score"]


def test_scoring_config_version_present():
    assert "version" in SCORING
    assert SCORING["earnings_weight"] == 0.75
