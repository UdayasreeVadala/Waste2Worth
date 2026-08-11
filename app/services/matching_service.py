from math import atan2, cos, radians, sin, sqrt

from app.services.pricing_service import calculate_farmer_earning, calculate_transport_cost

def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(earth_radius * c, 2)

def find_best_buyers(waste, buyers):
    matches = []

    for buyer in buyers:
        if buyer.max_capacity_kg < waste.quantity_kg:
            continue

        distance = calculate_distance(
            waste.latitude,
            waste.longitude,
            buyer.latitude,
            buyer.longitude
        )

        transport_cost = calculate_transport_cost(distance, waste.quantity_kg)

        farmer_earning = calculate_farmer_earning(
            waste.quantity_kg,
            buyer.price_per_kg,
            transport_cost
        )

        matches.append({
            "buyer_id": buyer.id,
            "business_name": buyer.business_name,
            "buyer_type": buyer.buyer_type,
            "distance_km": distance,
            "transport_cost": transport_cost,
            "farmer_earning": farmer_earning
        })

    return sorted(matches, key=lambda item: item["farmer_earning"], reverse=True)