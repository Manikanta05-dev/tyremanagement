from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.inventory import TireInventoryCreate, TireInventoryUpdate, TireInventoryResponse
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/all", response_model=List[TireInventoryResponse])
def get_all_inventory(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    inventory_service = InventoryService(db)
    return inventory_service.get_all_inventory(skip, limit, search)

@router.get("/{inventory_id}", response_model=TireInventoryResponse)
def get_inventory(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    inventory_service = InventoryService(db)
    return inventory_service.get_inventory_by_id(inventory_id)

@router.post("/add", response_model=TireInventoryResponse)
def add_inventory(
    inventory_data: TireInventoryCreate,
    db: Session = Depends(get_db)
):
    inventory_service = InventoryService(db)
    return inventory_service.create_inventory(inventory_data)

@router.put("/update/{inventory_id}", response_model=TireInventoryResponse)
def update_inventory(
    inventory_id: int,
    inventory_data: TireInventoryUpdate,
    db: Session = Depends(get_db)
):
    inventory_service = InventoryService(db)
    return inventory_service.update_inventory(inventory_id, inventory_data)

@router.delete("/delete/{inventory_id}")
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    inventory_service = InventoryService(db)
    return inventory_service.delete_inventory(inventory_id)
