from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.db.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    waste_id = Column(Integer, ForeignKey("waste_listings.id"), nullable=False, index=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False, index=True)
    buyer_name = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    explanation = Column(Text, nullable=True)
    buyer_offer = Column(Float, nullable=True)
    transport_cost = Column(Float, nullable=True)
    platform_fee = Column(Float, nullable=True)
    supplier_earning = Column(Float, nullable=True)
    price_per_kg = Column(Float, nullable=True)
    currency = Column(String, nullable=False, default="INR")
    status = Column(String, nullable=False, default="match_found")
    created_at = Column(DateTime, default=datetime.utcnow)