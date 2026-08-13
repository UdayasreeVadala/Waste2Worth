from datetime import datetime

from pydantic import BaseModel


class MatchCreate(BaseModel):
    waste_id: int
    buyer_id: int


class MatchResponse(BaseModel):
    id: int
    waste_id: int
    buyer_id: int
    buyer_name: str | None = None
    score: float | None = None
    explanation: str | None = None
    buyer_offer: float | None = None
    transport_cost: float | None = None
    platform_fee: float | None = None
    supplier_earning: float | None = None
    price_per_kg: float | None = None
    currency: str
    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True