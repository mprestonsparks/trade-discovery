from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, JSON
from .base import Base

class AssetPool(Base):
    __tablename__ = "asset_pool"

    symbol = Column(String(20), primary_key=True)
    asset_type = Column(String(20))
    exchange = Column(String(20))
    is_active = Column(Boolean, default=True)
    filters = Column(JSON)
    metadata = Column(JSON)
    last_updated = Column(DateTime)
