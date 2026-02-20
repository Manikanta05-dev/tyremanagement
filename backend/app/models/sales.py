from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class PaymentMode(str, enum.Enum):
    CASH = "cash"
    UPI = "upi"
    CARD = "card"

class Sales(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, unique=True, nullable=False, index=True)
    customer_name = Column(String, nullable=False)
    customer_mobile = Column(String, nullable=False)
    subtotal = Column(Float, nullable=False, default=0)  # Total before discount
    discount_type = Column(String, nullable=True)  # 'flat' or 'percent'
    discount_value = Column(Float, nullable=True, default=0)  # Discount amount or percentage
    discount_amount = Column(Float, nullable=True, default=0)  # Actual discount applied
    total_amount = Column(Float, nullable=False)  # Final amount after discount
    notes = Column(String, nullable=True)  # Optional notes
    payment_mode = Column(Enum(PaymentMode), nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    items = relationship("SalesItem", back_populates="sale", cascade="all, delete-orphan")

class SalesItem(Base):
    __tablename__ = "sales_items"
    
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    tire_id = Column(Integer, ForeignKey("tire_inventory.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    sale = relationship("Sales", back_populates="items")
    tire = relationship("TireInventory", back_populates="sales_items")
