from sqlalchemy import Column, Integer, Float, String, ForeignKey

from app.db.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    waste_id = Column(Integer, ForeignKey("waste_listings.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    transport_cost = Column(Float, nullable=False)
    farmer_earning = Column(Float, nullable=False)
    status = Column(String, default="pending")