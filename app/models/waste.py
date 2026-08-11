from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.db.database import Base

class WasteListing(Base):
    __tablename__ = "waste_listings"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    produce_type = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    photo_url = Column(String, nullable=True)
    status = Column(String, default="available")