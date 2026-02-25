from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseUpdate, PurchaseResponse
from app.services.purchase_service import PurchaseService

router = APIRouter(prefix="/purchase", tags=["Purchase"])

@router.post("/add", response_model=PurchaseResponse)
def add_purchase(
    purchase_data: PurchaseCreate,
    db: Session = Depends(get_db)
):
    purchase_service = PurchaseService(db)
    return purchase_service.create_purchase(purchase_data)

@router.get("/all", response_model=List[PurchaseResponse])
def get_all_purchases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    purchase_service = PurchaseService(db)
    return purchase_service.get_all_purchases(skip, limit)

@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    purchase_service = PurchaseService(db)
    return purchase_service.get_purchase_by_id(purchase_id)

@router.put("/update/{purchase_id}", response_model=PurchaseResponse)
def update_purchase(
    purchase_id: int,
    purchase_data: PurchaseUpdate,
    db: Session = Depends(get_db)
):
    purchase_service = PurchaseService(db)
    return purchase_service.update_purchase(purchase_id, purchase_data)

@router.delete("/delete/{purchase_id}")
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    purchase_service = PurchaseService(db)
    return purchase_service.delete_purchase(purchase_id)
