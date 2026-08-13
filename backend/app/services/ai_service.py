from waste2worth_ai.errors import ContractError
from waste2worth_ai.pipeline import evaluate_waste_opportunity

_FALLBACK_COORDS = {"latitude": 19.9975, "longitude": 73.7898}


def analyze_waste_listing(waste, buyers):
    return evaluate_waste_opportunity(
        waste_input=_waste_to_ai_input(waste),
        buyers=[_buyer_to_ai_input(buyer) for buyer in buyers],
    )


def evaluate_for_buyer(waste, buyer):
    result = evaluate_waste_opportunity(
        waste_input=_waste_to_ai_input(waste),
        buyers=[_buyer_to_ai_input(buyer)],
    )
    best = result["best_buyer"]
    if best is None or best["buyer_id"] != str(buyer.id):
        return None
    return best


def _waste_to_ai_input(waste):
    return {
        "supplier_id": str(waste.supplier_id),
        "waste_type": waste.produce_type,
        "quantity_kg": waste.quantity_kg,
        "condition": waste.condition or "unknown",
        "location": {
            "address": waste.location,
            "latitude": waste.latitude,
            "longitude": waste.longitude,
        },
        "notes": waste.notes,
        "available_from": waste.available_from,
        "available_until": waste.available_until,
        "photo_url": waste.photo_url,
    }


def _buyer_to_ai_input(buyer):
    capacity = (
        buyer.current_capacity_kg
        if getattr(buyer, "current_capacity_kg", None) is not None
        else buyer.max_capacity_kg
    )
    return {
        "id": str(buyer.id),
        "name": buyer.business_name,
        "business_type": buyer.buyer_type,
        "location": {
            "address": buyer.location,
            "latitude": buyer.latitude if buyer.latitude is not None else _FALLBACK_COORDS["latitude"],
            "longitude": buyer.longitude if buyer.longitude is not None else _FALLBACK_COORDS["longitude"],
        },
        "accepted_waste": _accepted_waste_types(buyer),
        "min_quantity_kg": getattr(buyer, "min_quantity_kg", 0) or 0,
        "max_quantity_kg": buyer.max_capacity_kg,
        "current_capacity_kg": capacity,
        "price_per_kg": buyer.price_per_kg,
        "currency": getattr(buyer, "currency", "INR") or "INR",
        "pickup_available": bool(getattr(buyer, "pickup_available", True)),
        "service_radius_km": getattr(buyer, "service_radius_km", None),
        "availability_status": getattr(buyer, "availability_status", "available") or "available",
    }


def _accepted_waste_types(buyer):
    explicit_types = getattr(buyer, "accepted_waste_types", None)
    if explicit_types:
        return [
            item.strip().lower()
            for item in explicit_types.split(",")
            if item.strip()
        ]

    buyer_type = (buyer.buyer_type or "").lower()

    if "biochar" in buyer_type:
        return ["wood", "dry_crop_residue", "grain", "crop", "coconut_shell"]

    return ["organic", "vegetable", "fruit", "food", "tomato", "crop", "produce"]