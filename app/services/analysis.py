"""
Analysis service for market state identification and opportunity scoring.
Integrates with market-analysis system for consistent state handling.
"""

from typing import Dict, Any, List, Optional
import numpy as np
from datetime import datetime
from market_analysis import MarketAnalyzer
from market_analysis.config import get_indicator_config
from sqlalchemy.orm import Session
from ..models.opportunities import Opportunity
from ..models.asset_pool import AssetPool

class AnalysisService:
    def __init__(self):
        self.config = get_indicator_config()
        
    async def analyze_asset(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single asset using market-analysis system's PCA-based state identification.
        
        Args:
            symbol: Asset symbol
            market_data: Market data for the asset
            
        Returns:
            Dict containing analysis results including market state and metrics
        """
        try:
            # Initialize market analyzer with configuration
            analyzer = MarketAnalyzer(symbol)
            
            # Set market data
            analyzer.data = market_data
            
            # Calculate technical indicators
            analyzer.calculate_technical_indicators()
            
            # Identify market states using PCA
            analyzer.identify_market_states()
            
            # Generate trading signals
            signals = analyzer.generate_trading_signals()
            
            # Extract state characteristics
            state_info = {
                'state': analyzer.current_state,  # Numeric state from PCA
                'characteristics': analyzer.state_characteristics[analyzer.current_state],
                'confidence': float(signals['confidence'][-1])
            }
            
            # Calculate opportunity score
            score = self._calculate_opportunity_score(
                state_info,
                signals,
                analyzer.technical_indicators
            )
            
            return {
                'symbol': symbol,
                'timestamp': datetime.utcnow(),
                'market_state': analyzer.current_state,  # Numeric state
                'confidence': state_info['confidence'],
                'score': score,
                'technical_metrics': {
                    'rsi': float(analyzer.technical_indicators['rsi'].iloc[-1]),
                    'macd': float(analyzer.technical_indicators['macd'].iloc[-1]),
                    'macd_signal': float(analyzer.technical_indicators['macd_signal'].iloc[-1]),
                    'stoch_k': float(analyzer.technical_indicators['stoch_k'].iloc[-1]),
                    'stoch_d': float(analyzer.technical_indicators['stoch_d'].iloc[-1])
                },
                'active_inference_metrics': {
                    'composite_signal': float(signals['composite_signal'][-1]),
                    'state_characteristics': state_info['characteristics']
                },
                'risk_metrics': {
                    'volatility': float(state_info['characteristics']['volatility']),
                    'trend_strength': float(state_info['characteristics']['trend_strength']),
                    'volume': float(state_info['characteristics']['volume']),
                    'return_dispersion': float(state_info['characteristics']['return_dispersion'])
                }
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing asset {symbol}: {str(e)}")
    
    def _calculate_opportunity_score(
        self,
        state_info: Dict[str, Any],
        signals: Dict[str, Any],
        technical_indicators: Dict[str, Any]
    ) -> float:
        """
        Calculate opportunity score based on state characteristics and signals.
        """
        # Get state characteristics
        volatility = state_info['characteristics']['volatility']
        trend_strength = state_info['characteristics']['trend_strength']
        volume = state_info['characteristics']['volume']
        
        # Get signal strength
        signal_strength = abs(signals['composite_signal'][-1])
        
        # Calculate score components
        trend_score = trend_strength * 0.4
        signal_score = signal_strength * 0.3
        volume_score = volume * 0.2
        confidence_score = state_info['confidence'] * 0.1
        
        # Penalize high volatility
        volatility_penalty = max(0, volatility - 0.5) * 0.2
        
        # Combine scores
        total_score = (trend_score + signal_score + volume_score + confidence_score) * (1 - volatility_penalty)
        
        return float(np.clip(total_score, 0, 1))
