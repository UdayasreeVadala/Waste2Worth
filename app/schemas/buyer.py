from pydantic import BaseModel

class BuyerCreate(BaseModel):
    business_name: str
    buyer_type: str
    location: str
    latitude: float
    longitude: float
    price_per_kg: float
    max_capacity_kg: float

class BuyerResponse(BuyerCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True