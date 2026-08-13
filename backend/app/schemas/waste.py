from datetime import datetime

from pydantic import BaseModel


class WasteCreate(BaseModel):
    produce_type: str
    quantity_kg: float
    condition: str = "unknown"
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    notes: str | None = None
    available_from: str | None = None
    available_until: str | None = None
    photo_url: str | None = None


class WasteUpdate(BaseModel):
    produce_type: str | None = None
    quantity_kg: float | None = None
    condition: str | None = None
    location: str | None = None
    notes: str | None = None
    available_from: str | None = None
    available_until: str | None = None
    photo_url: str | None = None


class WasteResponse(BaseModel):
    id: int
    supplier_id: int
    produce_type: str
    quantity_kg: float
    condition: str
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    notes: str | None = None
    available_from: str | None = None
    available_until: str | None = None
    photo_url: str | None = None
    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True