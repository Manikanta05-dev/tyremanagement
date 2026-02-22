import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, inventory, sales, dashboard, reports, purchase, invoice, profit
from app.core.database import engine, Base
from app.models import User, Supplier, TireInventory, Sales, SalesItem, Purchase, PurchaseItem

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize admin user
try:
    from init_db import init_admin
    init_admin()
except Exception as e:
    print(f"Warning: Could not initialize admin user: {e}")

app = FastAPI(
    title="Tire Shop Management API",
    description="API for managing tire inventory, sales, purchases, and invoicing",
    version="2.0.0"
)

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Add Vercel domains
vercel_origins = [
    "https://tyremanagement-git-main-manikanta05-devs-projects.vercel.app",
    "https://*.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173"
]

# Combine origins
all_origins = vercel_origins + [o for o in origins if o and o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins if all_origins else ["*"],
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
