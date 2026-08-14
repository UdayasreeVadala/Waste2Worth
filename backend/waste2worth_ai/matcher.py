from waste2worth_ai.pricing import estimate_margin
from waste2worth_ai.scoring_config import SCORING


def rank_buyers(waste_analysis, buyers):
    ranked = []
    for buyer in buyers:
        if not _is_suitable(waste_analysis, buyer):
            continue

        margin = estimate_margin(
            quantity_kg=waste_analysis["quantity_kg"],
            price_per_kg=buyer.price_per_kg,
            distance_km=buyer.distance_km,
            pickup_available=buyer.pickup_available,
            currency=buyer.currency,
        )
        score = _score(buyer, margin)
        ranked.append(
            {
                "buyer_id": buyer.id,
                "name": buyer.name,
                "business_type": buyer.business_type,
                "distance_km": buyer.distance_km,
                "price_per_kg": buyer.price_per_kg,
                "currency": buyer.currency,
                "pickup_available": buyer.pickup_available,
                "current_capacity_kg": buyer.current_capacity_kg,
                "estimated_margin": margin,
                "score": score,
                "factor_breakdown": _factor_breakdown(buyer, margin),
                "explanation": _explain_match(buyer, margin),
            }
        )

    return sorted(ranked, key=lambda row: row["score"], reverse=True)


def _is_suitable(waste_analysis, buyer):
    within_service_radius = (
        buyer.service_radius_km is None
        or buyer.distance_km is None
        or buyer.distance_km <= buyer.service_radius_km
    )

    waste_type = waste_analysis["waste_type"]
    category = waste_analysis.get("category", "").lower()
    accepts_type = (
        waste_type in buyer.accepted_waste
        or category in buyer.accepted_waste
        or "organic" in buyer.accepted_waste
    )

    capacity = buyer.current_capacity_kg if buyer.current_capacity_kg is not None else buyer.max_quantity_kg

    return (
        buyer.availability_status in {"available", "limited"}
        and accepts_type
        and buyer.min_quantity_kg <= waste_analysis["quantity_kg"] <= buyer.max_quantity_kg
        and capacity >= waste_analysis["quantity_kg"]
        and within_service_radius
    )


def _score(buyer, margin):
    earnings_points = margin["estimated_supplier_earnings"] * SCORING["earnings_weight"]
    distance_points = max(0, SCORING["distance_floor_km"] - (buyer.distance_km or SCORING["distance_floor_km"]))
    pickup_points = SCORING["pickup_bonus"] if buyer.pickup_available else 0
    capacity_points = min(
        (buyer.current_capacity_kg or 0) / 100 * SCORING["capacity_bonus_per_100_kg"],
        SCORING["capacity_bonus_cap"],
    )
    availability_points = (
        SCORING["availability_available"]
        if buyer.availability_status == "available"
        else SCORING["availability_limited"]
    )

    return round(
        (earnings_points * 1.0)
        + (distance_points * SCORING["distance_weight"])
        + pickup_points
        + capacity_points
        + availability_points,
        2,
    )


def _factor_breakdown(buyer, margin):
    earnings_points = margin["estimated_supplier_earnings"] * SCORING["earnings_weight"]
    distance_points = max(0, SCORING["distance_floor_km"] - (buyer.distance_km or SCORING["distance_floor_km"]))
    pickup_points = SCORING["pickup_bonus"] if buyer.pickup_available else 0
    capacity_points = min(
        (buyer.current_capacity_kg or 0) / 100 * SCORING["capacity_bonus_per_100_kg"],
        SCORING["capacity_bonus_cap"],
    )
    availability_points = (
        SCORING["availability_available"]
        if buyer.availability_status == "available"
        else SCORING["availability_limited"]
    )
    return {
        "earnings_points": round(earnings_points, 2),
        "distance_points": round(distance_points * SCORING["distance_weight"], 2),
        "pickup_points": pickup_points,
        "capacity_points": round(capacity_points, 2),
        "availability_points": availability_points,
        "version": SCORING["version"],
    }


def _explain_match(buyer, margin):
    pickup = "pickup is available" if buyer.pickup_available else "supplier delivery may be needed"
    return (
        f"{buyer.name} accepts this waste, has enough active capacity, {pickup}, "
        f"and the estimated supplier earning is {margin['currency']} "
        f"{margin['estimated_supplier_earnings']}."
    )
