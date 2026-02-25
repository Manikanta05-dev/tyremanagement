import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, inventory, sales, dashboard, reports, purchase, invoice, profit, debug
from app.core.database import engine, Base
from app.core.config import settings
from app.models import User, Supplier, TireInventory, Sales, SalesItem, Purchase, PurchaseItem

app = FastAPI(
    title="Tire Shop Management API",
    description="API for managing tire inventory, sales, purchases, and invoicing",
    version="2.0.0"
)

# CORS middleware - Read from environment
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# Log CORS origins for debugging
print(f"🌐 CORS Configuration:")
print(f"   Raw ALLOWED_ORIGINS: {repr(allowed_origins_str)}")
print(f"   Parsed origins: {allowed_origins}")
print(f"   Total origins: {len(allowed_origins)}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Only use configured origins (no wildcard with credentials)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global OPTIONS handler for CORS preflight requests
from fastapi.responses import Response

@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    """
    Handle CORS preflight OPTIONS requests.
    This ensures browser preflight requests get proper CORS headers.
    """
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",  # Will be overridden by CORS middleware
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Startup event - Create tables
@app.on_event("startup")
def startup_event():
    """Create database tables on application startup"""
    print("🚀 Starting up Tire Shop Management API...")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'local'}")
    
    # Import all models to ensure they're registered with Base
    from app.models import (
        User, UserRole, 
        Supplier, 
        TireInventory, TireType,
        Sales, SalesItem, PaymentMode,
        Purchase, PurchaseItem, PaymentStatus
    )
    
    # Check if we're in production environment
    environment = os.getenv("ENVIRONMENT", "development")
    is_production = environment == "production"
    
    # Handle schema migration for production
    if is_production:
        print("🔧 Production environment detected - checking for schema updates...")
        try:
            # Drop users table if it exists (to handle schema changes)
            print("🗑️ Dropping users table to apply schema updates...")
            User.__table__.drop(bind=engine, checkfirst=True)
            print("✅ Users table dropped successfully")
        except Exception as e:
            print(f"⚠️ Could not drop users table: {e}")
            print("   (This is normal if table doesn't exist yet)")
    
    # Create all tables
    try:
        print("📝 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # List created tables
        tables = Base.metadata.tables.keys()
        print(f"📋 Tables: {', '.join(tables)}")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print(f"⚠️ Application will continue but database operations may fail")
        import traceback
        traceback.print_exc()

# Include routers
app.include_router(auth.router)
app.include_router(inventory.router)
app.include_router(sales.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(purchase.router)
app.include_router(invoice.router)
app.include_router(profit.router)
app.include_router(debug.router)

@app.get("/")
def root():
    return {
        "message": "Tire Shop Management API v2.0",
        "status": "running",
        "features": [
            "Inventory Management",
            "Sales Management",
            "Purchase Management",
            "GST Invoice Generation",
            "Profit Calculation",
            "Daily Closing Reports",
            "WhatsApp Integration"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/db-status")
def database_status():
    """Check database connection and tables"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {
            "status": "connected",
            "tables": tables,
            "table_count": len(tables)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
