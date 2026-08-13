from waste2worth_ai.pricing import estimate_margin


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
    net = margin["estimated_supplier_earnings"]
    distance_score = max(0, 80 - (buyer.distance_km or 80))
    pickup_score = 30 if buyer.pickup_available else 0
    capacity_score = min(buyer.current_capacity_kg / 100, 25)
    availability_score = 12 if buyer.availability_status == "available" else 4
    return round((net * 0.75) + (distance_score * 1.1) + pickup_score + capacity_score + availability_score, 2)


def _explain_match(buyer, margin):
    pickup = "pickup is available" if buyer.pickup_available else "supplier delivery may be needed"
    return (
        f"{buyer.name} accepts this waste, has enough active capacity, {pickup}, "
        f"and the estimated supplier earning is {margin['currency']} "
        f"{margin['estimated_supplier_earnings']}."
    )
