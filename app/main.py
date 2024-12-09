from fastapi import FastAPI
from .api.routes import router
from .db.database import engine
from .models import base, opportunities, asset_pool, historical_performance
import os
from dotenv import load_dotenv

load_dotenv()

# Create database tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trade Discovery Service",
    description="A service for discovering and ranking trading opportunities",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "service": "Trade Discovery",
        "status": "running",
        "version": "1.0.0"
    }
