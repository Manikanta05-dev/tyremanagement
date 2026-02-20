from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, inventory, sales, dashboard, reports, purchase, invoice, profit
from app.core.database import engine, Base
from app.models import User, Supplier, TireInventory, Sales, SalesItem, Purchase, PurchaseItem

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tire Shop Management API",
    description="API for managing tire inventory, sales, purchases, and invoicing",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
