from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.db.database import Base

class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    business_name = Column(String, nullable=False)
    buyer_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    price_per_kg = Column(Float, nullable=False)
    max_capacity_kg = Column(Float, nullable=False)