from datetime import datetime

from pydantic import BaseModel


class TransactionResponse(BaseModel):
    id: int
    match_id: int | None = None
    supplier_id: int
    buyer_user_id: int
    buyer_profile_id: int | None = None
    waste_id: int
    waste_type: str
    quantity_kg: float
    currency: str
    final_price: float | None = None
    transport_cost: float | None = None
    platform_fee: float | None = None
    supplier_earning: float | None = None
    pickup_method: str | None = None
    pickup_date: str | None = None
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class SchedulePickupRequest(BaseModel):
    pickup_method: str = "buyer_pickup"
    pickup_date: str | None = None


class BuyerRespondRequest(BaseModel):
    action: str  # accept | reject | offer
    price: float | None = None
    pickup_included: bool | None = None