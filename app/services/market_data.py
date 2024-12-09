"""
Market data service for fetching data from Interactive Brokers.
"""

import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
from ib_insync import IB, Contract, util
from ..config import settings

class MarketDataService:
    def __init__(self):
        self.ib = IB()
        self._connect()
        
    def _connect(self):
        """Connect to Interactive Brokers TWS/Gateway"""
        try:
            self.ib.connect(
                host=settings.IB_HOST,
                port=settings.IB_PORT,
                clientId=settings.IB_CLIENT_ID,
                readonly=True  # Read-only since we're just fetching data
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Interactive Brokers: {str(e)}")
    
    async def get_market_data(self, symbol: str, lookback_days: int = 30) -> Dict[str, Any]:
        """
        Fetch historical market data for analysis.
        
        Args:
            symbol: Trading symbol (e.g., 'AAPL')
            lookback_days: Number of days of historical data to fetch
            
        Returns:
            Dictionary containing market data and metadata
        """
        try:
            # Create stock contract
            contract = Contract(
                symbol=symbol,
                secType='STK',
                exchange='SMART',
                currency='USD'
            )
            
            # Get end time (now) and start time
            end_time = datetime.now()
            start_time = end_time - timedelta(days=lookback_days)
            
            # Fetch historical data
            bars = await self.ib.reqHistoricalDataAsync(
                contract,
                endDateTime=end_time,
                durationStr=f'{lookback_days} D',
                barSizeSetting='1 day',
                whatToShow='TRADES',
                useRTH=True
            )
            
            # Convert to DataFrame
            df = util.df(bars)
            
            # Get latest price
            latest_price = await self._get_latest_price(contract)
            
            return {
                'symbol': symbol,
                'timestamp': datetime.utcnow(),
                'latest_price': latest_price,
                'historical_data': df.to_dict('records'),
                'metadata': {
                    'start_time': start_time,
                    'end_time': end_time,
                    'source': 'Interactive Brokers',
                    'timeframe': '1D'
                }
            }
            
        except Exception as e:
            raise Exception(f"Error fetching market data for {symbol}: {str(e)}")
            
    async def _get_latest_price(self, contract: Contract) -> float:
        """Get the latest price for a contract"""
        ticker = self.ib.reqMktData(contract)
        await asyncio.sleep(1)  # Wait for data to arrive
        return ticker.last if ticker.last else ticker.close
        
    def disconnect(self):
        """Disconnect from Interactive Brokers"""
        self.ib.disconnect()
