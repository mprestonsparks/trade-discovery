"""
Configuration settings for the trade discovery service.
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '5432'))
    DB_NAME: str = os.getenv('DB_NAME', 'trade_discovery')
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    
    # Interactive Brokers settings
    IB_HOST: str = os.getenv('IB_HOST', 'localhost')
    IB_PORT: int = int(os.getenv('IB_PORT', '7497'))  # 7497 for paper trading, 7496 for live
    IB_CLIENT_ID: int = int(os.getenv('IB_CLIENT_ID', '1'))
