from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.sales import PaymentMode

class SalesItemCreate(BaseModel):
    tire_id: int
    quantity: int

class SalesItemResponse(BaseModel):
    id: int
    tire_id: int
    quantity: int
    unit_price: float
    total_price: float
    tire_brand: str
    tire_size: str
    
    class Config:
        from_attributes = True

class SalesCreate(BaseModel):
    customer_name: str
    customer_mobile: str
    payment_mode: PaymentMode
    items: List[SalesItemCreate]
    discount_type: Optional[str] = None  # 'flat' or 'percent'
    discount_value: float = 0  # Discount amount or percentage
    notes: Optional[str] = None  # Optional notes

class SalesResponse(BaseModel):
    id: int
    invoice_id: str
    customer_name: str
    customer_mobile: str
    subtotal: float = 0
    discount_type: Optional[str] = None
    discount_value: float = 0
    discount_amount: float = 0
    total_amount: float
    notes: Optional[str] = None
    payment_mode: PaymentMode
    sale_date: datetime
    items: List[SalesItemResponse]
    
    class Config:
        from_attributes = True
