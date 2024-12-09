from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from .base import Base

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    market_state = Column(Integer)
    confidence = Column(Float)
    score = Column(Float, index=True)
    technical_metrics = Column(JSON)
    active_inference_metrics = Column(JSON)
    risk_metrics = Column(JSON)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
