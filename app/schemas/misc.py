from datetime import datetime
from typing import Optional, List
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import BaseSchema
from app.schemas.product import Product


class SupplierBase(BaseSchema):
    """Base supplier schema."""
    name: str = Field(..., min_length=1, max_length=100)
    contact_info: str = Field(..., min_length=5, max_length=100)
    product_list: Optional[List[Product]] = None


class SupplierCreate(SupplierBase):
    """Schema for creating a supplier."""
    pass


class SupplierUpdate(BaseSchema):
    """Schema for updating a supplier."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    contact_info: Optional[str] = Field(None, min_length=5, max_length=100)
    product_list: Optional[List[Product]] = None


class Supplier(SupplierBase):
    """Supplier schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class PurchaseOrderStatusEnum(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"


class PurchaseOrderBase(BaseSchema):
    """Base purchase order schema."""
    supplier_id: UUID
    product_list: Optional[List[dict]] = Field(default=[], description="List of products")
    status: PurchaseOrderStatusEnum = PurchaseOrderStatusEnum.PENDING


class PurchaseOrderCreate(PurchaseOrderBase):
    """Schema for creating a purchase order."""
    pass


class PurchaseOrderUpdate(BaseSchema):
    """Schema for updating a purchase order."""
    supplier_id: Optional[UUID] = None
    product_list: Optional[List[dict]] = Field(None, description="List of products")
    status: Optional[PurchaseOrderStatusEnum] = None


class PurchaseOrder(PurchaseOrderBase):
    """Purchase order schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class DiscountTypeEnum(str, Enum):
    PERCENTAGE = "Percentage"
    FIXED_AMOUNT = "FixedAmount"


class DiscountBase(BaseSchema):
    """Base discount schema."""
    name: str = Field(..., min_length=1, max_length=100)
    type: DiscountTypeEnum
    value: float = Field(..., ge=0)
    applicable_products: Optional[List[UUID]] = None


class DiscountCreate(DiscountBase):
    """Schema for creating a discount."""
    pass


class DiscountUpdate(BaseSchema):
    """Schema for updating a discount."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[DiscountTypeEnum] = None
    value: Optional[float] = Field(None, ge=0)
    applicable_products: Optional[List[UUID]] = None


class Discount(DiscountBase):
    """Discount schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class SettingsBase(BaseSchema):
    """Base settings schema."""
    key: str = Field(..., min_length=1, max_length=100)
    value: str


class SettingsCreate(SettingsBase):
    """Schema for creating a setting."""
    pass


class SettingsUpdate(BaseSchema):
    """Schema for updating a setting."""
    key: Optional[str] = Field(None, min_length=1, max_length=100)
    value: Optional[str] = None


class Settings(SettingsBase):
    """Settings schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class NotificationBase(BaseSchema):
    """Base notification schema."""
    type: str = Field(..., min_length=1, max_length=50)
    message: str = Field(..., min_length=1, max_length=500)
    timestamp: datetime


class NotificationCreate(NotificationBase):
    """Schema for creating a notification."""
    pass


class NotificationUpdate(BaseSchema):
    """Schema for updating a notification."""
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    message: Optional[str] = Field(None, min_length=1, max_length=500)
    timestamp: Optional[datetime] = None


class Notification(NotificationBase):
    """Notification schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class SalesReportFilter(BaseSchema):
    """Sales report filter schema."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    customer_id: Optional[UUID] = None
    product_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None


class SalesReportData(BaseSchema):
    """Sales report data schema."""
    total_revenue: float = Field(..., ge=0)
    total_sales_count: int = Field(..., ge=0)
    top_products: List[dict] = []
    sales_by_date: List[dict] = []
    customer_analytics: List[dict] = []


class SalesReportBase(BaseSchema):
    """Base sales report schema."""
    total_sales: float = Field(..., ge=0)
    total_transactions: int = Field(..., ge=0)
    sales_by_product: List[dict]


class SalesReport(SalesReportBase):
    """Sales report schema."""
    pass
