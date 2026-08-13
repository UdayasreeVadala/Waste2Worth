from pydantic import BaseModel


class AgentContactRequest(BaseModel):
    minimum_total_price: float
    requires_pickup: bool = True
    allow_counter_offer: bool = True
    supplier_approved_contact: bool = True


class AgentContactResponse(BaseModel):
    status: str
    events: list[str]
    deal: dict | None = None

