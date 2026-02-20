from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class PaymentStatus(str, enum.Enum):
    PAID = "paid"
    PENDING = "pending"

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    purchase_date = Column(Date, nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Relationships
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")
