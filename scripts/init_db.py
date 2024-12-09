from app.db.database import engine
from app.models.base import Base
from app.models import opportunities, asset_pool, historical_performance

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
