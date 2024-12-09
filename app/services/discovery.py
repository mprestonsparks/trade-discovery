"""
Discovery service for managing asset pool analysis and opportunity tracking.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from sqlalchemy.orm import Session
from .analysis import AnalysisService
from .market_data import MarketDataService
from ..models.opportunities import Opportunity
from ..models.asset_pool import AssetPool

class DiscoveryService:
    def __init__(self):
        self.analysis_service = AnalysisService()
        self.market_data_service = MarketDataService()
        self.batch_size = 100
        
    async def analyze_asset_pool(self, db: Session) -> List[Dict[str, Any]]:
        """
        Analyze all active assets in the pool.
        
        Args:
            db: Database session
            
        Returns:
            List of analysis results
        """
        try:
            # Get all active assets
            assets = db.query(AssetPool).filter(AssetPool.is_active == True).all()
            
            # Process assets in batches
            results = []
            for i in range(0, len(assets), self.batch_size):
                batch = assets[i:i + self.batch_size]
                batch_results = await asyncio.gather(*[
                    self._process_asset(asset, db)
                    for asset in batch
                ])
                results.extend([r for r in batch_results if r is not None])
            
            return results
            
        except Exception as e:
            raise Exception(f"Error analyzing asset pool: {str(e)}")
        finally:
            self.market_data_service.disconnect()
    
    async def _process_asset(self, asset: AssetPool, db: Session) -> Optional[Dict[str, Any]]:
        """
        Process a single asset and store results.
        
        Args:
            asset: Asset to analyze
            db: Database session
            
        Returns:
            Analysis results if successful, None otherwise
        """
        try:
            # Get market data from Interactive Brokers
            market_data = await self.market_data_service.get_market_data(asset.symbol)
            
            # Analyze asset
            analysis_result = await self.analysis_service.analyze_asset(
                asset.symbol,
                market_data
            )
            
            # Create opportunity record
            opportunity = Opportunity(
                symbol=asset.symbol,
                timestamp=analysis_result['timestamp'],
                market_state=analysis_result['market_state'],
                confidence=analysis_result['confidence'],
                score=analysis_result['score'],
                technical_metrics=analysis_result['technical_metrics'],
                active_inference_metrics=analysis_result['active_inference_metrics'],
                risk_metrics=analysis_result['risk_metrics'],
                metadata={
                    'analysis_version': '1.0',
                    'asset_type': asset.asset_type,
                    'exchange': asset.exchange
                }
            )
            
            db.add(opportunity)
            db.commit()
            
            return analysis_result
            
        except Exception as e:
            # Log error but continue processing other assets
            print(f"Error processing asset {asset.symbol}: {str(e)}")
            return None
