from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.db.database import Base


class WasteListing(Base):
    __tablename__ = "waste_listings"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    produce_type = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    condition = Column(String, nullable=False, default="unknown")
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    available_from = Column(String, nullable=True)
    available_until = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    status = Column(String, nullable=False, default="available")
    created_at = Column(DateTime, default=datetime.utcnow)