from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.inventory import TireInventory
from app.models.supplier import Supplier

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[TireInventory]:
        query = self.db.query(TireInventory)
        if search:
            query = query.filter(
                or_(
                    TireInventory.brand.ilike(f"%{search}%"),
                    TireInventory.tire_size.ilike(f"%{search}%")
                )
            )
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, inventory_id: int) -> Optional[TireInventory]:
        return self.db.query(TireInventory).filter(TireInventory.id == inventory_id).first()
    
    def create(self, inventory_data: dict) -> TireInventory:
        inventory = TireInventory(**inventory_data)
        self.db.add(inventory)
        self.db.commit()
        self.db.refresh(inventory)
        return inventory
    
    def update(self, inventory_id: int, inventory_data: dict) -> Optional[TireInventory]:
        inventory = self.get_by_id(inventory_id)
        if inventory:
            for key, value in inventory_data.items():
                if value is not None:
                    setattr(inventory, key, value)
            self.db.commit()
            self.db.refresh(inventory)
        return inventory
    
    def delete(self, inventory_id: int) -> bool:
        inventory = self.get_by_id(inventory_id)
        if inventory:
            self.db.delete(inventory)
            self.db.commit()
            return True
        return False
    
    def update_quantity(self, inventory_id: int, quantity_change: int) -> Optional[TireInventory]:
        inventory = self.get_by_id(inventory_id)
        if inventory:
            inventory.quantity += quantity_change
            self.db.commit()
            self.db.refresh(inventory)
        return inventory
    
    def get_low_stock(self, threshold: int = 5) -> List[TireInventory]:
        return self.db.query(TireInventory).filter(TireInventory.quantity < threshold).all()
    
    def get_total_inventory_value(self) -> float:
        items = self.db.query(TireInventory).all()
        return sum(item.selling_price * item.quantity for item in items)
