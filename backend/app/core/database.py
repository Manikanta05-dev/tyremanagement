from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# Read DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

print(f"🔌 Connecting to database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'local'}")

# Determine if SSL is required (Render PostgreSQL)
use_ssl = False
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    # Check if we're on Render (dpg- prefix or render.com in URL)
    if "render.com" in DATABASE_URL or "dpg-" in DATABASE_URL:
        use_ssl = True
        print("🔒 SSL mode enabled for Render PostgreSQL")

# Create engine with SSL support for production
if use_ssl:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"},
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=300,    # Recycle connections after 5 minutes
        echo=False,          # Set to True for SQL query logging
    )
else:
    # Local development or SQLite
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
