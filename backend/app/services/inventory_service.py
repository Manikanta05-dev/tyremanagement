from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory import TireInventoryCreate, TireInventoryUpdate, TireInventoryResponse

class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_repo = InventoryRepository(db)
    
    def get_all_inventory(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[TireInventoryResponse]:
        items = self.inventory_repo.get_all(skip, limit, search)
        return [self._to_response(item) for item in items]
    
    def get_inventory_by_id(self, inventory_id: int) -> TireInventoryResponse:
        item = self.inventory_repo.get_by_id(inventory_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
        return self._to_response(item)
    
    def create_inventory(self, inventory_data: TireInventoryCreate) -> TireInventoryResponse:
        item = self.inventory_repo.create(inventory_data.model_dump())
        return self._to_response(item)
    
    def update_inventory(self, inventory_id: int, inventory_data: TireInventoryUpdate) -> TireInventoryResponse:
        update_data = inventory_data.model_dump(exclude_unset=True)
        item = self.inventory_repo.update(inventory_id, update_data)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
        return self._to_response(item)
    
    def delete_inventory(self, inventory_id: int) -> dict:
        success = self.inventory_repo.delete(inventory_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
        return {"message": "Inventory item deleted successfully"}
    
    def _to_response(self, item) -> TireInventoryResponse:
        response_data = {
            "id": item.id,
            "brand": item.brand,
            "tire_size": item.tire_size,
            "tire_type": item.tire_type,
            "quantity": item.quantity,
            "purchase_price": item.purchase_price,
            "selling_price": item.selling_price,
            "supplier_id": item.supplier_id,
            "purchase_date": item.purchase_date,
            "supplier_name": item.supplier.name if item.supplier else None
        }
        return TireInventoryResponse(**response_data)
