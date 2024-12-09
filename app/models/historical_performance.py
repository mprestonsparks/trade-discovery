from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, JSON, ForeignKey
from .base import Base

class HistoricalPerformance(Base):
    __tablename__ = "historical_performance"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    actual_return = Column(Float)
    prediction_accuracy = Column(Float)
    market_impact = Column(Float)
    metadata = Column(JSON)
    evaluated_at = Column(DateTime, default=datetime.utcnow)
