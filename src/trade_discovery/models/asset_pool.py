"""
Models for asset pool management.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .base import Base

class AssetPool(Base):
    __tablename__ = "asset_pool"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    active = Column(Boolean, default=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    last_analyzed = Column(DateTime, nullable=True)
