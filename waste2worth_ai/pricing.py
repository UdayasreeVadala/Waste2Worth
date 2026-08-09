def estimate_margin(quantity_kg, price_per_kg, distance_km, pickup_available, currency, platform_fee_rate=0.03):
    buyer_offer = round(quantity_kg * price_per_kg, 2)
    transport_cost = 0.0 if pickup_available else round(distance_km * 1.4, 2)
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

