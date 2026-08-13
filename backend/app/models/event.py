from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text

from app.db.database import Base


class TransactionEvent(Base):
    __tablename__ = "transaction_events"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    actor = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    payload = Column(JSON, nullable=True, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)