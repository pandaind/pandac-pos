from sqlalchemy import Column, String, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Product(BaseModel):
    """Product model."""
    __tablename__ = "products"

    name = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)
    discount_id = Column(UUID(as_uuid=True), ForeignKey("discounts.id"), nullable=True)
    
    # Relationships
    discount = relationship("Discount", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)


class Inventory(BaseModel):
    """Inventory model."""
    __tablename__ = "inventories"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, unique=True)
    quantity = Column(Float, nullable=False, default=0)
    reorder_level = Column(Float, nullable=False, default=0)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True)
    
    # Relationships
    product = relationship("Product", back_populates="inventory")
    supplier = relationship("Supplier", back_populates="inventories")
