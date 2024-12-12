"""
FastAPI application for trade discovery service.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from .api.routes import router
from .db.database import engine
from .models import base

# Create database tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trade Discovery Service",
    description="A service for discovering and ranking trading opportunities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Prometheus instrumentation
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="trade_discovery_requests_inprogress",
    inprogress_labels=True,
)

# Add custom metrics
@instrumentator.counter(
    name="trade_discovery_opportunities_total",
    documentation="Total number of trading opportunities discovered",
    labels={"strategy": "default"}
)
def opportunities_total():
    return 0

@instrumentator.histogram(
    name="trade_discovery_scan_duration_seconds",
    documentation="Duration of market scanning operations",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)
def scan_duration():
    return 0

@instrumentator.gauge(
    name="trade_discovery_active_assets",
    documentation="Number of assets currently being monitored",
)
def active_assets():
    return 0  # This will be updated by the asset pool service

# Initialize and instrument
instrumentator.instrument(app).expose(app, include_in_schema=True, tags=["Monitoring"])

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "service": "Trade Discovery",
        "status": "running",
        "version": "1.0.0"
    }
