import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, inventory, sales, dashboard, reports, purchase, invoice, profit
from app.core.database import engine, Base
from app.core.config import settings
from app.models import User, Supplier, TireInventory, Sales, SalesItem, Purchase, PurchaseItem

app = FastAPI(
    title="Tire Shop Management API",
    description="API for managing tire inventory, sales, purchases, and invoicing",
    version="2.0.0"
)

# CORS middleware - Read from environment
allowed_origins = settings.ALLOWED_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins + ["*"],  # Allow configured origins + wildcard for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event - Create tables
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting up...")
    print(f"📊 Database URL: {settings.DATABASE_URL[:50]}...")
    
    # Create all tables
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Error creating tables: {e}")

# Include routers
app.include_router(auth.router)
app.include_router(inventory.router)
app.include_router(sales.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(purchase.router)
app.include_router(invoice.router)
app.include_router(profit.router)

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
