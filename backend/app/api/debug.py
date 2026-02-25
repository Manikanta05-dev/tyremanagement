from fastapi import APIRouter
from sqlalchemy import text
from app.core.database import SessionLocal, engine
import traceback

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/db_status")
def database_status():
    """
    Database health check endpoint for production debugging.
    
    Checks:
    1. Database connection
    2. Users table existence
    3. Basic query execution
    """
    db = None
    try:
        # Create database session
        db = SessionLocal()
        
        # Test 1: Simple query to verify connection
        result = db.execute(text("SELECT 1")).scalar()
        if result != 1:
            return {
                "database": "error",
                "message": "Query returned unexpected result"
            }
        
        # Test 2: Check if users table exists
        table_check = db.execute(
            text("SELECT to_regclass('public.users')")
        ).scalar()
        
        if table_check is None:
            return {
                "database": "connected",
                "users_table": "missing",
                "message": "Database connected but users table does not exist"
            }
        
        # Test 3: Count users (optional verification)
        user_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
        
        return {
            "database": "connected",
            "users_table": "exists",
            "user_count": user_count,
            "message": "Database and users table are healthy"
        }
        
    except Exception as e:
        error_details = {
            "database": "error",
            "message": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        return error_details
        
    finally:
        if db:
            db.close()

@router.get("/tables")
def list_tables():
    """List all tables in the database"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {
            "status": "success",
            "tables": tables,
            "table_count": len(tables)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }

@router.get("/connection_info")
def connection_info():
    """Get database connection information (sanitized)"""
    try:
        from app.core.config import settings
        import os
        
        # Read DATABASE_URL
        db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
        
        # Check if SSL is enabled
        ssl_enabled = False
        if db_url and db_url.startswith("postgresql://"):
            if "render.com" in db_url or "dpg-" in db_url:
                ssl_enabled = True
        
        # Sanitize DATABASE_URL to hide password
        if "@" in db_url:
            # Format: postgresql://user:password@host:port/database
            parts = db_url.split("@")
            host_part = parts[1] if len(parts) > 1 else "unknown"
            protocol = parts[0].split("://")[0] if "://" in parts[0] else "unknown"
            
            return {
                "status": "success",
                "protocol": protocol,
                "host": host_part,
                "ssl_enabled": ssl_enabled,
                "is_render": "render.com" in db_url or "dpg-" in db_url
            }
        else:
            return {
                "status": "success",
                "message": "Local database",
                "ssl_enabled": False
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/cors_config")
def cors_configuration():
    """Get CORS configuration for debugging"""
    try:
        import os
        
        # Read ALLOWED_ORIGINS
        allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")
        allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]
        
        return {
            "status": "success",
            "raw_value": allowed_origins_str,
            "parsed_origins": allowed_origins,
            "total_origins": len(allowed_origins),
            "has_whitespace": any(" " in origin for origin in allowed_origins_str.split(",")),
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
