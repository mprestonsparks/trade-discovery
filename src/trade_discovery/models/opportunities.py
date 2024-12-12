"""
Models for trading opportunities.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from .base import Base

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    score = Column(Float)
    market_state = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metrics = Column(JSON)  # Store additional metrics as JSON
    analysis = Column(JSON)  # Store detailed analysis as JSON
