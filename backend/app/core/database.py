from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# Handle Render PostgreSQL SSL requirement
database_url = settings.DATABASE_URL

# Add SSL mode for production (Render requires SSL)
if database_url and database_url.startswith("postgresql://"):
    # Check if we're on Render (or any production environment)
    if "render" in database_url or os.getenv("RENDER"):
        # Add SSL mode if not already present
        if "sslmode" not in database_url:
            database_url = database_url + ("&" if "?" in database_url else "?") + "sslmode=require"
            print("🔒 Added SSL mode to database connection")

print(f"🔌 Connecting to database: {database_url.split('@')[1] if '@' in database_url else 'local'}")

# Create engine with SSL support
engine = create_engine(
    database_url,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=300,    # Recycle connections after 5 minutes
    echo=False,          # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
