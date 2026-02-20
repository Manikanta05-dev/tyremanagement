from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class TireType(str, enum.Enum):
    TUBE = "tube"
    TUBELESS = "tubeless"

class TireInventory(Base):
    __tablename__ = "tire_inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False, index=True)
    tire_size = Column(String, nullable=False)
    tire_type = Column(Enum(TireType), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    purchase_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    purchase_date = Column(Date, nullable=False)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="inventory_items")
    sales_items = relationship("SalesItem", back_populates="tire")
