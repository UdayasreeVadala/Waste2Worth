from pydantic import BaseModel

class WasteCreate(BaseModel):
    produce_type: str
    quantity_kg: float
    location: str
    latitude: float
    longitude: float
    photo_url: str | None = None

class WasteResponse(WasteCreate):
    id: int
    farmer_id: int
    status: str

    class Config:
        from_attributes = True