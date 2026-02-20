from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem

class PurchaseRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Purchase]:
        return self.db.query(Purchase).order_by(Purchase.purchase_date.desc()).offset(skip).limit(limit).all()
    
    def get_by_id(self, purchase_id: int) -> Optional[Purchase]:
        return self.db.query(Purchase).filter(Purchase.id == purchase_id).first()
    
    def create(self, purchase_data: dict, items_data: List[dict]) -> Purchase:
        purchase = Purchase(**purchase_data)
        self.db.add(purchase)
        self.db.flush()
        
        for item_data in items_data:
            item = PurchaseItem(purchase_id=purchase.id, **item_data)
            self.db.add(item)
        
        self.db.commit()
        self.db.refresh(purchase)
        return purchase
    
    def update(self, purchase_id: int, purchase_data: dict) -> Optional[Purchase]:
        purchase = self.get_by_id(purchase_id)
        if purchase:
            for key, value in purchase_data.items():
                if value is not None:
                    setattr(purchase, key, value)
            self.db.commit()
            self.db.refresh(purchase)
        return purchase
    
    def delete(self, purchase_id: int) -> bool:
        purchase = self.get_by_id(purchase_id)
        if purchase:
            self.db.delete(purchase)
            self.db.commit()
            return True
        return False
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Purchase]:
        return self.db.query(Purchase).filter(
            Purchase.purchase_date >= start_date,
            Purchase.purchase_date <= end_date
        ).all()
