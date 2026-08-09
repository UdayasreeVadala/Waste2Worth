from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WasteInput:
    supplier_id: str | None
    waste_type: str
    quantity_kg: float
    condition: str
    location: dict[str, Any]
    available_from: str | None = None
    available_until: str | None = None
    photo_url: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class BuyerProfile:
    id: str
    name: str
    business_type: str
    location: dict[str, Any]
    distance_km: float | None
    accepted_waste: list[str]
    min_quantity_kg: float
    max_quantity_kg: float
    current_capacity_kg: float
    price_per_kg: float
    currency: str
    pickup_available: bool
    service_radius_km: float | None
    availability_status: str
    last_updated: str | None = None


@dataclass(frozen=True)
class SupplierRules:
    minimum_total_price: float
    requires_pickup: bool
    allow_counter_offer: bool = True
