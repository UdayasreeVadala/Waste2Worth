from datetime import datetime

from pydantic import BaseModel


class TransactionEventResponse(BaseModel):
    id: int
    transaction_id: int | None = None
    match_id: int | None = None
    event_type: str
    actor: str
    message: str | None = None
    payload: dict | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True