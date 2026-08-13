from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=True, index=True)
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    buyer_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    buyer_profile_id = Column(Integer, ForeignKey("buyers.id"), nullable=True)
    waste_id = Column(Integer, ForeignKey("waste_listings.id"), nullable=False, index=True)
    waste_type = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="INR")

    final_price = Column(Float, nullable=True)
    transport_cost = Column(Float, nullable=True)
    platform_fee = Column(Float, nullable=True)
    supplier_earning = Column(Float, nullable=True)

    pickup_method = Column(String, nullable=True)
    pickup_date = Column(String, nullable=True)

    status = Column(String, nullable=False, default="match_found")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)