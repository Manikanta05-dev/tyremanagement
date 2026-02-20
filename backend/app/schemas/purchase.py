from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.models.purchase import PaymentStatus

class PurchaseItemCreate(BaseModel):
    tire_id: int
    quantity: int
    purchase_price: float

class PurchaseItemResponse(BaseModel):
    id: int
    tire_id: int
    quantity: int
    purchase_price: float
    total_price: float
    tire_brand: str
    tire_size: str
    
    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    supplier_name: str
    purchase_date: date
    payment_status: PaymentStatus = PaymentStatus.PENDING

class PurchaseCreate(PurchaseBase):
    items: List[PurchaseItemCreate]

class PurchaseUpdate(BaseModel):
    supplier_name: Optional[str] = None
    purchase_date: Optional[date] = None
    payment_status: Optional[PaymentStatus] = None

class PurchaseResponse(PurchaseBase):
    id: int
    total_amount: float
    items: List[PurchaseItemResponse]
    
    class Config:
        from_attributes = True
