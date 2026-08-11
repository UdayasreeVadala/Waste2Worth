from pydantic import BaseModel

class BuyerCreate(BaseModel):
    business_name: str
    buyer_type: str
    location: str
    latitude: float
    longitude: float
    price_per_kg: float
    max_capacity_kg: float
    accepted_waste_types: str = "organic,vegetable,fruit,food,crop,produce"
    min_quantity_kg: float = 0
    current_capacity_kg: float | None = None
    pickup_available: bool = True
    service_radius_km: float | None = None
    availability_status: str = "available"
    currency: str = "INR"

class BuyerResponse(BuyerCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
