from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.db.database import Base


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    business_name = Column(String, nullable=False)
    buyer_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    price_per_kg = Column(Float, nullable=False)
    min_quantity_kg = Column(Float, nullable=False, default=0)
    max_capacity_kg = Column(Float, nullable=False)
    current_capacity_kg = Column(Float, nullable=True)
    accepted_waste_types = Column(String, default="organic,vegetable,fruit,food,crop,produce")
    pickup_available = Column(Boolean, nullable=False, default=True)
    service_radius_km = Column(Float, nullable=True)
    availability_status = Column(String, nullable=False, default="available")
    currency = Column(String, nullable=False, default="INR")
    requirement_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)