from datetime import datetime

from pydantic import BaseModel


class BuyerCreate(BaseModel):
    business_name: str
    buyer_type: str
    location: str
    latitude: float | None = None
    longitude: float | None = None
    price_per_kg: float
    max_capacity_kg: float
    accepted_waste_types: str = "organic,vegetable,fruit,food,crop,produce"
    min_quantity_kg: float = 0
    current_capacity_kg: float | None = None
    pickup_available: bool = True
    service_radius_km: float | None = None
    availability_status: str = "available"
    currency: str = "INR"
    requirement_notes: str | None = None


class BuyerUpdate(BaseModel):
    business_name: str | None = None
    buyer_type: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    price_per_kg: float | None = None
    max_capacity_kg: float | None = None
    accepted_waste_types: str | None = None
    min_quantity_kg: float | None = None
    current_capacity_kg: float | None = None
    pickup_available: bool | None = None
    service_radius_km: float | None = None
    availability_status: str | None = None
    currency: str | None = None
    requirement_notes: str | None = None


class BuyerResponse(BaseModel):
    id: int
    owner_id: int
    business_name: str
    buyer_type: str
    location: str
    latitude: float | None = None
    longitude: float | None = None
    price_per_kg: float
    max_capacity_kg: float
    accepted_waste_types: str
    min_quantity_kg: float
    current_capacity_kg: float | None = None
    pickup_available: bool
    service_radius_km: float | None = None
    availability_status: str
    currency: str
    requirement_notes: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True