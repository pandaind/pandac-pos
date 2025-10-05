from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import BaseSchema
from app.schemas.product import Product


class CustomerBase(BaseSchema):
    """Base customer schema."""
    name: str = Field(..., min_length=1, max_length=100)
    contact_info: str = Field(..., min_length=5, max_length=100)
    loyalty_points: int = Field(default=0, ge=0)


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""
    pass


class CustomerUpdate(BaseSchema):
    """Schema for updating a customer."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    contact_info: Optional[str] = Field(None, min_length=5, max_length=100)
    loyalty_points: Optional[int] = Field(None, ge=0)


class Customer(CustomerBase):
    """Customer schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class SaleBase(BaseSchema):
    """Base sale schema."""
    customer_id: UUID
    total_amount: float = Field(..., ge=0)
    product_list: List[Product] = Field(..., min_items=1)
    discount_id: Optional[UUID] = None


class SaleCreate(SaleBase):
    """Schema for creating a sale."""
    pass


class SaleUpdate(BaseSchema):
    """Schema for updating a sale."""
    customer_id: Optional[UUID] = None
    total_amount: Optional[float] = Field(None, ge=0)
    product_list: Optional[List[Product]] = Field(None, min_items=1)
    discount_id: Optional[UUID] = None


class Sale(SaleBase):
    """Sale schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class LoyaltyProgramBase(BaseSchema):
    """Base loyalty program schema."""
    customer_id: UUID
    points: int = Field(default=0, ge=0)
    tier: str = Field(default="Bronze")


class LoyaltyProgramCreate(LoyaltyProgramBase):
    """Schema for creating a loyalty program."""
    pass


class LoyaltyProgramUpdate(BaseSchema):
    """Schema for updating a loyalty program."""
    points: Optional[int] = Field(None, ge=0)
    tier: Optional[str] = None


class LoyaltyProgram(LoyaltyProgramBase):
    """Loyalty program schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime
