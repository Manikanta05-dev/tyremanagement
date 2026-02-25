from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.schemas.sales import SalesResponse
from app.schemas.inventory import TireInventoryResponse
from app.services.sales_service import SalesService
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/sales", response_model=List[SalesResponse])
def get_sales_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    sales_service = SalesService(db)
    return sales_service.get_sales_report(start_date, end_date)

@router.get("/inventory", response_model=List[TireInventoryResponse])
def get_inventory_report(
    db: Session = Depends(get_db)
):
    inventory_service = InventoryService(db)
    return inventory_service.get_all_inventory(limit=10000)
