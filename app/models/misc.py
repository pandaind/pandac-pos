from sqlalchemy import Column, String, Float, ForeignKey, Enum, JSON, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class PurchaseOrderStatusEnum(enum.Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"


class DiscountTypeEnum(enum.Enum):
    PERCENTAGE = "Percentage"
    FIXED_AMOUNT = "FixedAmount"


class PurchaseOrder(BaseModel):
    """Purchase order model."""
    __tablename__ = "purchase_orders"

    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=False)
    product_list = Column(JSON, nullable=False)  # Store product list as JSON
    status = Column(Enum(PurchaseOrderStatusEnum), nullable=False, default=PurchaseOrderStatusEnum.PENDING)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="purchase_orders")


class Discount(BaseModel):
    """Discount model."""
    __tablename__ = "discounts"

    name = Column(String(100), nullable=False)
    type = Column(Enum(DiscountTypeEnum), nullable=False)
    value = Column(Float, nullable=False)
    applicable_products = Column(JSON, nullable=True)  # Store product IDs as JSON array
    
    # Relationships
    products = relationship("Product", back_populates="discount")


class Settings(BaseModel):
    """Settings model."""
    __tablename__ = "settings"

    key = Column(String(100), nullable=False, unique=True, index=True)
    value = Column(Text, nullable=False)


class Notification(BaseModel):
    """Notification model."""
    __tablename__ = "notifications"

    type = Column(String(50), nullable=False)
    message = Column(String(500), nullable=False)
    timestamp = Column(DateTime, nullable=False)
