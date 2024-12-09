# Trade Discovery Service

## Overview

The Trade Discovery Service is a microservice designed to automate the discovery of trading opportunities across a large pool of assets. It integrates with the existing market-analysis and trade-manager systems, utilizing their proven analysis capabilities while focusing on opportunity identification and ranking rather than trade execution.

## System Architecture

### High-Level Design
```
[Trade Discovery Service]
├── Asset Pool Management
│   └── Configurable asset lists and filters
├── Analysis Orchestration
│   ├── Market Analysis Integration
│   │   └── PCA/Technical Analysis
│   └── Trade Manager Integration
│       └── Active Inference/GA Analysis
├── Results Database
│   ├── Opportunities
│   ├── Rankings
│   └── Historical Performance
└── API Layer
    └── Endpoints for trade-manager queries
```

### Integration Flow
```
[Discovery Service]
    │
    ├── Pulls market data for asset pool
    │   │
    │   ├── Feeds to Market Analysis
    │   │   └── PCA/Technical Analysis
    │   │
    │   └── Feeds to Trade Manager
    │       └── Active Inference/GA Analysis
    │
    └── Writes to Database
        ├── Opportunity Scores
        ├── Market States
        └── Risk Metrics

[Trade Manager]
    │
    └── Queries Discovery Service
        └── Selects best opportunities
            based on current portfolio
```

## Integration Requirements

### Market Analysis Integration

The service must integrate with the market-analysis system's key components:

1. **PCA Analysis**
   - Uses existing PCA implementation for market state identification
   - Required imports from market-analysis:
     ```python
     from market_analysis import MarketAnalyzer
     from market_analysis.config import get_indicator_config
     ```

2. **Technical Indicators**
   - Leverages existing technical analysis infrastructure
   - Key indicators used:
     - RSI
     - MACD
     - Stochastic Oscillator
     - Bollinger Bands

3. **Market State Identification**
   - Uses the existing state classification system
   - Maintains consistency with market-analysis project's state definitions

### Trade Manager Integration

Integration with trade-manager's active inference and genetic algorithm systems:

1. **Active Inference**
   - Uses existing belief updating framework
   - Required imports from trade-manager:
     ```python
     from trade_manager.strategy import ActiveInferenceOptimizer
     from trade_manager.core import SystemState
     ```

2. **Genetic Algorithms**
   - Leverages existing optimization framework
   - Uses same fitness evaluation criteria

## Database Schema

### Opportunities Table
```sql
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    market_state VARCHAR(50),
    confidence DECIMAL(5,4),
    score DECIMAL(10,4),
    technical_metrics JSONB,
    active_inference_metrics JSONB,
    risk_metrics JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_opportunities_symbol ON opportunities(symbol);
CREATE INDEX idx_opportunities_timestamp ON opportunities(timestamp);
CREATE INDEX idx_opportunities_score ON opportunities(score);
```

### Asset Pool Table
```sql
CREATE TABLE asset_pool (
    symbol VARCHAR(20) PRIMARY KEY,
    asset_type VARCHAR(20),
    exchange VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    filters JSONB,
    metadata JSONB,
    last_updated TIMESTAMP
);
```

### Historical Performance Table
```sql
CREATE TABLE historical_performance (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id),
    actual_return DECIMAL(10,4),
    prediction_accuracy DECIMAL(5,4),
    market_impact DECIMAL(10,4),
    metadata JSONB,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Discovery Service API

1. **Get Current Opportunities**
   ```
   GET /api/v1/opportunities
   Query Parameters:
   - min_score: float
   - market_state: string
   - limit: int
   - offset: int
   ```

2. **Get Asset Details**
   ```
   GET /api/v1/assets/{symbol}
   Response: Detailed analysis and current opportunities
   ```

3. **Update Asset Pool**
   ```
   POST /api/v1/asset-pool
   Body: List of assets and their configurations
   ```

4. **Get Historical Performance**
   ```
   GET /api/v1/performance/{symbol}
   Query Parameters:
   - start_date: timestamp
   - end_date: timestamp
   ```

## Configuration

### Environment Variables
```
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trade_discovery
DB_USER=postgres
DB_PASSWORD=your_password

# Service Configuration
ASSET_POOL_UPDATE_INTERVAL=3600  # seconds
ANALYSIS_BATCH_SIZE=100
MAX_CONCURRENT_ANALYSES=10

# Integration Points
MARKET_ANALYSIS_HOST=localhost
MARKET_ANALYSIS_PORT=8000
TRADE_MANAGER_HOST=localhost
TRADE_MANAGER_PORT=8001

# API Configuration
API_PORT=8002
API_HOST=0.0.0.0
```

### Asset Pool Configuration
```yaml
asset_pool:
  default_filters:
    min_market_cap: 1000000000  # $1B
    min_volume: 1000000  # Daily volume
    exchanges:
      - NYSE
      - NASDAQ
  update_schedule: "0 0 * * *"  # Daily at midnight
  batch_size: 100
```

### Analysis Configuration
```yaml
analysis:
  timeframes:
    - 1d
    - 4h
    - 1h
  indicators:
    rsi:
      enabled: true
      period: 14
    macd:
      enabled: true
      fast_period: 12
      slow_period: 26
      signal_period: 9
  market_states:
    min_confidence: 0.6
    state_hold_time: 3600  # seconds
```

## Development Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Access to market-analysis and trade-manager repositories

### Required Python Packages
```
# requirements.txt
fastapi>=0.68.0
uvicorn>=0.15.0
sqlalchemy>=1.4.23
psycopg2-binary>=2.9.1
pydantic>=1.8.2
numpy>=1.21.2
pandas>=1.3.3
pytest>=6.2.5
requests>=2.26.0
python-dotenv>=0.19.0
asyncio>=3.4.3
aiohttp>=3.7.4
```

### Installation Steps
1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up database:
   ```bash
   psql -U postgres -f scripts/init_db.sql
   ```
5. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

### Running Tests
```bash
pytest tests/
```

### Starting the Service
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

## Deployment

### Docker Support
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  trade-discovery:
    build: .
    ports:
      - "8002:8002"
    environment:
      - DB_HOST=db
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: trade_discovery
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## Project Structure
```
trade-discovery/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── discovery.py
│   │   ├── analysis.py
│   │   └── integration.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_services.py
├── scripts/
│   └── init_db.sql
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Implementation Guidelines

1. **Error Handling**
   - Implement comprehensive error handling for all integrations
   - Log all errors with appropriate context
   - Implement retry mechanisms for external service calls

2. **Performance Considerations**
   - Use connection pooling for database operations
   - Implement caching where appropriate
   - Use batch processing for asset analysis
   - Implement rate limiting for external API calls

3. **Monitoring**
   - Log key metrics:
     - Analysis duration
     - Success/failure rates
     - API response times
   - Implement health check endpoints
   - Track resource usage

4. **Security**
   - Implement API authentication
   - Use environment variables for sensitive data
   - Validate all input data
   - Implement rate limiting

## Future Enhancements

1. **Machine Learning Integration**
   - Add ML models for opportunity scoring
   - Implement pattern recognition
   - Add anomaly detection

2. **Advanced Analytics**
   - Add correlation analysis across assets
   - Implement sector/industry analysis
   - Add sentiment analysis

3. **Performance Optimization**
   - Add caching layer
   - Implement parallel processing
   - Add real-time updates

4. **UI Dashboard**
   - Add visualization of opportunities
   - Add configuration interface
   - Add performance metrics display
