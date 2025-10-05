from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import BaseSchema


class ProductBase(BaseSchema):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    discount_id: Optional[UUID] = None


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass


class ProductUpdate(BaseSchema):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    discount_id: Optional[UUID] = None


class Product(ProductBase):
    """Product schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class InventoryBase(BaseSchema):
    """Base inventory schema."""
    product_id: UUID
    quantity: int = Field(..., ge=0)
    reorder_level: int = Field(..., ge=0)
    supplier_id: Optional[UUID] = None


class InventoryCreate(InventoryBase):
    """Schema for creating an inventory item."""
    pass


class InventoryUpdate(BaseSchema):
    """Schema for updating an inventory item."""
    quantity: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    supplier_id: Optional[UUID] = None


class Inventory(InventoryBase):
    """Inventory schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime
