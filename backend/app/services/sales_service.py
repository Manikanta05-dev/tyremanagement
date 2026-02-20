from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from datetime import date
from app.repositories.sales_repository import SalesRepository
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.sales import SalesCreate, SalesResponse, SalesItemResponse

class SalesService:
    def __init__(self, db: Session):
        self.db = db
        self.sales_repo = SalesRepository(db)
        self.inventory_repo = InventoryRepository(db)
    
    def create_sale(self, sales_data: SalesCreate) -> SalesResponse:
        # Validate inventory and calculate totals
        subtotal = 0
        items_data = []
        
        for item in sales_data.items:
            tire = self.inventory_repo.get_by_id(item.tire_id)
            if not tire:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tire with id {item.tire_id} not found")
            
            if tire.quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {tire.brand} {tire.tire_size}. Available: {tire.quantity}"
                )
            
            item_total = tire.selling_price * item.quantity
            subtotal += item_total
            
            items_data.append({
                "tire_id": item.tire_id,
                "quantity": item.quantity,
                "unit_price": tire.selling_price,
                "total_price": item_total
            })
        
        # Calculate discount
        discount_amount = 0
        if sales_data.discount_value and sales_data.discount_value > 0:
            if sales_data.discount_type == 'percent':
                discount_amount = (subtotal * sales_data.discount_value) / 100
            else:  # flat
                discount_amount = sales_data.discount_value
        
        # Calculate final amount
        total_amount = subtotal - discount_amount
        
        # Generate invoice ID
        invoice_id = self.sales_repo.generate_invoice_id()
        
        # Create sale
        sale_dict = {
            "invoice_id": invoice_id,
            "customer_name": sales_data.customer_name,
            "customer_mobile": sales_data.customer_mobile,
            "subtotal": subtotal,
            "discount_type": sales_data.discount_type,
            "discount_value": sales_data.discount_value,
            "discount_amount": discount_amount,
            "total_amount": total_amount,
            "notes": sales_data.notes,
            "payment_mode": sales_data.payment_mode
        }
        
        sale = self.sales_repo.create(sale_dict, items_data)
        
        # Update inventory quantities
        for item in sales_data.items:
            self.inventory_repo.update_quantity(item.tire_id, -item.quantity)
        
        return self._to_response(sale)
    
    def get_sales_history(self, skip: int = 0, limit: int = 100) -> List[SalesResponse]:
        sales = self.sales_repo.get_all(skip, limit)
        return [self._to_response(sale) for sale in sales]
    
    def get_sale_by_id(self, sale_id: int) -> SalesResponse:
        sale = self.sales_repo.get_by_id(sale_id)
        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
        return self._to_response(sale)
    
    def get_sales_report(self, start_date: date, end_date: date) -> List[SalesResponse]:
        sales = self.sales_repo.get_by_date_range(start_date, end_date)
        return [self._to_response(sale) for sale in sales]
    
    def _to_response(self, sale) -> SalesResponse:
        items = [
            SalesItemResponse(
                id=item.id,
                tire_id=item.tire_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
                tire_brand=item.tire.brand,
                tire_size=item.tire.tire_size
            )
            for item in sale.items
        ]
        
        return SalesResponse(
            id=sale.id,
            invoice_id=sale.invoice_id,
            customer_name=sale.customer_name,
            customer_mobile=sale.customer_mobile,
            subtotal=sale.subtotal if hasattr(sale, 'subtotal') else sale.total_amount,
            discount_type=sale.discount_type if hasattr(sale, 'discount_type') else None,
            discount_value=sale.discount_value if hasattr(sale, 'discount_value') else 0,
            discount_amount=sale.discount_amount if hasattr(sale, 'discount_amount') else 0,
            total_amount=sale.total_amount,
            notes=sale.notes if hasattr(sale, 'notes') else None,
            payment_mode=sale.payment_mode,
            sale_date=sale.sale_date,
            items=items
        )
