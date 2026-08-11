from waste2worth_ai.pipeline import evaluate_waste_opportunity


def evaluate_waste_listing(waste, buyers):
    waste_input = {
        "supplier_id": str(waste.farmer_id),
        "waste_type": waste.produce_type,
        "quantity_kg": waste.quantity_kg,
        "condition": "unknown",
        "location": {
            "address": waste.location,
            "latitude": waste.latitude,
            "longitude": waste.longitude,
        },
        "photo_url": waste.photo_url,
    }

    buyer_inputs = [_buyer_to_ai_input(buyer) for buyer in buyers]
    return evaluate_waste_opportunity(waste_input=waste_input, buyers=buyer_inputs)


def find_ai_ranked_buyers(waste, buyers):
    ai_result = evaluate_waste_listing(waste, buyers)

    if ai_result["best_buyer"] is None:
        return []

    return [_match_response_from_ai_buyer(buyer) for buyer in ai_result["ranked_buyers"]]


def _buyer_to_ai_input(buyer):
    return {
        "id": str(buyer.id),
        "name": buyer.business_name,
        "business_type": buyer.buyer_type,
        "location": {
            "address": buyer.location,
            "latitude": buyer.latitude,
            "longitude": buyer.longitude,
        },
        "accepted_waste": _accepted_waste_types(buyer),
        "min_quantity_kg": 0,
        "max_quantity_kg": buyer.max_capacity_kg,
        "current_capacity_kg": buyer.max_capacity_kg,
        "price_per_kg": buyer.price_per_kg,
        "currency": "INR",
        "pickup_available": True,
        "service_radius_km": None,
        "availability_status": "available",
    }


def _accepted_waste_types(buyer):
    buyer_type = (buyer.buyer_type or "").lower()

    if "biochar" in buyer_type:
        return ["wood", "dry_crop_residue", "coconut_shell"]

    return ["tomato", "vegetable", "fruit", "food", "organic", "crop", "produce"]


def _match_response_from_ai_buyer(ai_buyer):
    margin = ai_buyer["estimated_margin"]
    return {
        "buyer_id": int(ai_buyer["buyer_id"]),
        "business_name": ai_buyer["name"],
        "buyer_type": ai_buyer["business_type"],
        "distance_km": ai_buyer["distance_km"],
        "transport_cost": margin["transport_cost"],
        "farmer_earning": margin["estimated_supplier_earnings"],
    }

