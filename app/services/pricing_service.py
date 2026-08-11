def calculate_transport_cost(distance_km: float, quantity_kg: float) -> float:
    cost_per_km = 8
    quantity_factor = quantity_kg * 0.5
    return round((distance_km * cost_per_km) + quantity_factor, 2)

def calculate_farmer_earning(
    quantity_kg: float,
    price_per_kg: float,
    transport_cost: float
) -> float:
    gross_amount = quantity_kg * price_per_kg
    return round(gross_amount - transport_cost, 2)