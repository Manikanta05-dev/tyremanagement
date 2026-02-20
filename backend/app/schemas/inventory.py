from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.inventory import TireType

class TireInventoryBase(BaseModel):
    brand: str
    tire_size: str
    tire_type: TireType
    quantity: int
    purchase_price: float
    selling_price: float
    supplier_id: Optional[int] = None
    purchase_date: date

class TireInventoryCreate(TireInventoryBase):
    pass

class TireInventoryUpdate(BaseModel):
    brand: Optional[str] = None
    tire_size: Optional[str] = None
    tire_type: Optional[TireType] = None
    quantity: Optional[int] = None
    purchase_price: Optional[float] = None
    selling_price: Optional[float] = None
    supplier_id: Optional[int] = None
    purchase_date: Optional[date] = None

class TireInventoryResponse(TireInventoryBase):
    id: int
    supplier_name: Optional[str] = None
    
    class Config:
        from_attributes = True
