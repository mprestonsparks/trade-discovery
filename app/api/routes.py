from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..db.database import get_db
from ..models.opportunities import Opportunity
from ..models.asset_pool import AssetPool
from ..services.discovery import DiscoveryService

router = APIRouter()
discovery_service = DiscoveryService()

@router.get("/opportunities")
async def get_opportunities(
    min_score: Optional[float] = Query(None),
    market_state: Optional[int] = Query(None),
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """
    Get trading opportunities with optional filtering.
    Market state is now an integer corresponding to PCA-identified states.
    """
    query = db.query(Opportunity)
    
    if min_score is not None:
        query = query.filter(Opportunity.score >= min_score)
    if market_state is not None:
        query = query.filter(Opportunity.market_state == market_state)
    
    opportunities = query.order_by(Opportunity.score.desc()).offset(offset).limit(limit).all()
    return opportunities

@router.get("/assets/{symbol}")
async def get_asset_details(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Get detailed analysis for a specific asset"""
    asset = db.query(AssetPool).filter(AssetPool.symbol == symbol).first()
    opportunities = db.query(Opportunity).filter(
        Opportunity.symbol == symbol
    ).order_by(
        Opportunity.timestamp.desc()
    ).limit(10).all()
    
    return {"asset": asset, "opportunities": opportunities}

@router.post("/asset-pool")
async def update_asset_pool(
    assets: List[dict],
    db: Session = Depends(get_db)
):
    """Update the asset pool configuration"""
    for asset_data in assets:
        asset = AssetPool(**asset_data)
        db.merge(asset)
    db.commit()
    return {"status": "success"}

@router.post("/analyze")
async def analyze_assets(db: Session = Depends(get_db)):
    """
    Trigger analysis of all active assets in the pool
    """
    try:
        results = await discovery_service.analyze_asset_pool(db)
        return {
            "status": "success",
            "analyzed_count": len(results),
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.utcnow()
        }
