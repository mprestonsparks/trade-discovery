# Trade Discovery Service


A microservice designed to automate the discovery of trading opportunities across a large pool of assets. This service integrates with existing market-analysis and trade-manager systems to identify and rank trading opportunities.

## Features

- Asset Pool Management with configurable filters
- Integration with Market Analysis (PCA/Technical Analysis)
- Integration with Trade Manager (Active Inference/GA Analysis)
- RESTful API for querying trading opportunities
- Historical performance tracking

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the root directory with the following variables:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trade_discovery
DB_USER=postgres
DB_PASSWORD=your_password

ASSET_POOL_UPDATE_INTERVAL=3600
ANALYSIS_BATCH_SIZE=100
MAX_CONCURRENT_ANALYSES=10

MARKET_ANALYSIS_HOST=localhost
MARKET_ANALYSIS_PORT=8000
TRADE_MANAGER_HOST=localhost
TRADE_MANAGER_PORT=8001

API_PORT=8002
API_HOST=0.0.0.0
```

4. Initialize the database:
```bash
python scripts/init_db.py
```

5. Start the service:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

## API Documentation

Once the service is running, visit `http://localhost:8002/docs` for the interactive API documentation.

## Project Structure

```
trade-discovery/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── services/
├── scripts/
├── tests/
├── docs/
├── .env
├── requirements.txt
└── README.md