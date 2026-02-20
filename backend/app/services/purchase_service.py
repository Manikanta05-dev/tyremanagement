from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.purchase import PurchaseCreate, PurchaseUpdate, PurchaseResponse, PurchaseItemResponse

class PurchaseService:
    def __init__(self, db: Session):
        self.db = db
        self.purchase_repo = PurchaseRepository(db)
        self.inventory_repo = InventoryRepository(db)
    
    def create_purchase(self, purchase_data: PurchaseCreate) -> PurchaseResponse:
        # Validate all tires exist and calculate total
        total_amount = 0
        items_data = []
        
        for item in purchase_data.items:
            tire = self.inventory_repo.get_by_id(item.tire_id)
            if not tire:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tire with id {item.tire_id} not found"
                )
            
            item_total = item.purchase_price * item.quantity
            total_amount += item_total
            
            items_data.append({
                "tire_id": item.tire_id,
                "quantity": item.quantity,
                "purchase_price": item.purchase_price,
                "total_price": item_total
            })
        
        # Create purchase with items
        purchase_dict = {
            "supplier_name": purchase_data.supplier_name,
            "total_amount": total_amount,
            "purchase_date": purchase_data.purchase_date,
            "payment_status": purchase_data.payment_status
        }
        
        purchase = self.purchase_repo.create(purchase_dict, items_data)
        
        # Update inventory quantities for all items
        for item in purchase_data.items:
            self.inventory_repo.update_quantity(item.tire_id, item.quantity)
        
        return self._to_response(purchase)
    
    def get_all_purchases(self, skip: int = 0, limit: int = 100) -> List[PurchaseResponse]:
        purchases = self.purchase_repo.get_all(skip, limit)
        return [self._to_response(purchase) for purchase in purchases]
    
    def get_purchase_by_id(self, purchase_id: int) -> PurchaseResponse:
        purchase = self.purchase_repo.get_by_id(purchase_id)
        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase not found"
            )
        return self._to_response(purchase)
    
    def update_purchase(self, purchase_id: int, purchase_data: PurchaseUpdate) -> PurchaseResponse:
        update_data = purchase_data.model_dump(exclude_unset=True)
        
        purchase = self.purchase_repo.update(purchase_id, update_data)
        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase not found"
            )
        return self._to_response(purchase)
    
    def delete_purchase(self, purchase_id: int) -> dict:
        success = self.purchase_repo.delete(purchase_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase not found"
            )
        return {"message": "Purchase deleted successfully"}
    
    def _to_response(self, purchase) -> PurchaseResponse:
        items = [
            PurchaseItemResponse(
                id=item.id,
                tire_id=item.tire_id,
                quantity=item.quantity,
                purchase_price=item.purchase_price,
                total_price=item.total_price,
                tire_brand=item.tire.brand,
                tire_size=item.tire.tire_size
            )
            for item in purchase.items
        ]
        
        return PurchaseResponse(
            id=purchase.id,
            supplier_name=purchase.supplier_name,
            total_amount=purchase.total_amount,
            purchase_date=purchase.purchase_date,
            payment_status=purchase.payment_status,
            items=items
        )
