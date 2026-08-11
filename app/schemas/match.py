from pydantic import BaseModel

class MatchResponse(BaseModel):
    buyer_id: int
    business_name: str
    buyer_type: str
    distance_km: float
    transport_cost: float
    farmer_earning: float