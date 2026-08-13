from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    transaction_id: int
    sender_id: int | None = None
    sender_role: str
    content: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True