from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)
    tire_id = Column(Integer, ForeignKey("tire_inventory.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    purchase = relationship("Purchase", back_populates="items")
    tire = relationship("TireInventory")
