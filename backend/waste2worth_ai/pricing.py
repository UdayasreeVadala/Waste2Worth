from waste2worth_ai import impact_factors as F


def estimate_margin(
    quantity_kg,
    price_per_kg,
    distance_km,
    pickup_available,
    currency,
    platform_fee_rate=F.PLATFORM_FEE_RATE,
):
    buyer_offer = round(quantity_kg * price_per_kg, 2)
    transport_cost = 0.0 if pickup_available else round((distance_km or 0) * F.TRANSPORT_COST_PER_KM, 2)
    platform_fee = round(buyer_offer * platform_fee_rate, 2)
    estimated_supplier_earnings = round(buyer_offer - transport_cost - platform_fee, 2)

    return {
        "currency": currency,
        "buyer_offer": buyer_offer,
        "transport_cost": transport_cost,
        "platform_fee": platform_fee,
        "estimated_supplier_earnings": estimated_supplier_earnings,
        "is_estimate": True,
    }
