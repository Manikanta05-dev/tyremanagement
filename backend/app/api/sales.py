from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.schemas.sales import SalesCreate, SalesResponse
from app.services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/create", response_model=SalesResponse)
def create_sale(
    sales_data: SalesCreate,
    db: Session = Depends(get_db)
):
    sales_service = SalesService(db)
    return sales_service.create_sale(sales_data)

@router.get("/history", response_model=List[SalesResponse])
def get_sales_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    sales_service = SalesService(db)
    return sales_service.get_sales_history(skip, limit)

@router.get("/{sale_id}", response_model=SalesResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    sales_service = SalesService(db)
    return sales_service.get_sale_by_id(sale_id)
