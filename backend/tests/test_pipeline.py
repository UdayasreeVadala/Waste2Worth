from waste2worth_ai.pipeline import evaluate_waste_opportunity
from waste2worth_ai.errors import ContractError


def test_full_pipeline_with_backend_buyer_data():
    result = evaluate_waste_opportunity(
        waste_input={
            "waste_type": "tomato",
            "quantity_kg": 700,
            "condition": "spoiled",
            "location": {"city": "Nashik", "country": "India"},
        },
        buyers=[
            {
                "id": "buyer_1",
                "name": "GreenBio Energy",
                "business_type": "Biogas plant",
                "location": {"city": "Nashik", "country": "India"},
                "distance_km": 25,
                "service_radius_km": 50,
                "accepted_waste": ["tomato", "vegetable"],
                "min_quantity_kg": 300,
                "max_quantity_kg": 3000,
                "current_capacity_kg": 1500,
                "price_per_kg": 0.3,
                "currency": "USD",
                "pickup_available": True,
                "availability_status": "available",
            }
        ],
    )

    assert result["analysis"]["display_name"] == "Tomato waste"
    assert result["recommended_use"]["recommended_route"] == "anaerobic_digestion"
    assert result["best_buyer"]["buyer_id"] == "buyer_1"
    assert result["requires_supplier_approval"] is True


def test_pipeline_returns_no_suitable_buyers():
    result = evaluate_waste_opportunity(
        waste_input={
            "waste_type": "tomato",
            "quantity_kg": 700,
            "condition": "spoiled",
            "location": {"city": "Nashik", "country": "India"},
        },
        buyers=[
            {
                "id": "buyer_wood",
                "name": "Wood Biochar",
                "business_type": "Biochar plant",
                "location": {"city": "Nashik", "country": "India"},
                "distance_km": 10,
                "accepted_waste": ["wood"],
                "min_quantity_kg": 100,
                "max_quantity_kg": 3000,
                "current_capacity_kg": 2000,
                "price_per_kg": 0.5,
                "currency": "USD",
                "pickup_available": True,
                "availability_status": "available",
            }
        ],
    )

    assert result["best_buyer"] is None
    assert result["agent_status"] == "no_suitable_buyers"
    assert result["error"]["code"] == "NO_SUITABLE_BUYERS"


def test_pipeline_filters_buyer_outside_service_radius():
    result = evaluate_waste_opportunity(
        waste_input={
            "waste_type": "tomato",
            "quantity_kg": 700,
            "condition": "spoiled",
            "location": {"city": "Nashik", "country": "India"},
        },
        buyers=[
            {
                "id": "buyer_far",
                "name": "Far Biogas",
                "business_type": "Biogas plant",
                "location": {"city": "Mumbai", "country": "India"},
                "distance_km": 170,
                "service_radius_km": 50,
                "accepted_waste": ["tomato"],
                "min_quantity_kg": 100,
                "max_quantity_kg": 3000,
                "current_capacity_kg": 2000,
                "price_per_kg": 0.7,
                "currency": "USD",
                "pickup_available": True,
                "availability_status": "available",
            }
        ],
    )

    assert result["best_buyer"] is None


def test_pipeline_calculates_distance_from_coordinates():
    result = evaluate_waste_opportunity(
        waste_input={
            "waste_type": "tomato",
            "quantity_kg": 700,
            "condition": "spoiled",
            "location": {"latitude": 19.9975, "longitude": 73.7898},
        },
        buyers=[
            {
                "id": "buyer_coords",
                "name": "Coordinate Biogas",
                "business_type": "Biogas plant",
                "location": {"latitude": 20.01, "longitude": 73.79},
                "accepted_waste": ["tomato"],
                "min_quantity_kg": 100,
                "max_quantity_kg": 3000,
                "current_capacity_kg": 2000,
                "price_per_kg": 0.3,
                "currency": "USD",
                "pickup_available": True,
                "service_radius_km": 50,
                "availability_status": "available",
            }
        ],
    )

    assert result["best_buyer"]["distance_km"] > 0


def test_pipeline_rejects_invalid_quantity():
    try:
        evaluate_waste_opportunity(
            waste_input={
                "waste_type": "tomato",
                "quantity_kg": 0,
                "condition": "spoiled",
                "location": {"city": "Nashik"},
            },
            buyers=[],
        )
    except ContractError as exc:
        assert exc.code == "INVALID_NUMBER"
        assert exc.field == "quantity_kg"
    else:
        raise AssertionError("Expected ContractError")
