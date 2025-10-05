from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum

from app.schemas.user import BaseSchema


# Enums
class SaleStatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethodEnum(str, Enum):
    CASH = "cash"
    CARD = "card"
    DIGITAL = "digital"
    CHECK = "check"


class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class DiscountTypeEnum(str, Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


# Sale Item Schemas
class SaleItemBase(BaseSchema):
    product_id: UUID
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    subtotal: float = Field(..., ge=0)
    discount_amount: Optional[float] = Field(0, ge=0)


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseSchema):
    product_id: Optional[UUID] = None
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, gt=0)
    subtotal: Optional[float] = Field(None, ge=0)
    discount_amount: Optional[float] = Field(None, ge=0)


class SaleItem(SaleItemBase):
    id: UUID
    sale_id: UUID
    created_at: datetime
    updated_at: datetime


# Sale Schemas
class SaleBase(BaseSchema):
    customer_id: Optional[UUID] = None
    cashier_id: UUID
    sale_date: datetime
    subtotal: float = Field(..., ge=0)
    tax_amount: float = Field(..., ge=0)
    discount_amount: float = Field(0, ge=0)
    total_amount: float = Field(..., ge=0)
    status: SaleStatusEnum = SaleStatusEnum.PENDING
    notes: Optional[str] = Field(None, max_length=500)


class SaleCreate(SaleBase):
    items: List[SaleItemCreate] = Field(..., min_items=1)


class SaleUpdate(BaseSchema):
    customer_id: Optional[UUID] = None
    cashier_id: Optional[UUID] = None
    sale_date: Optional[datetime] = None
    subtotal: Optional[float] = Field(None, ge=0)
    tax_amount: Optional[float] = Field(None, ge=0)
    discount_amount: Optional[float] = Field(None, ge=0)
    total_amount: Optional[float] = Field(None, ge=0)
    status: Optional[SaleStatusEnum] = None
    notes: Optional[str] = Field(None, max_length=500)


class Sale(SaleBase):
    id: UUID
    items: List[SaleItem] = []
    created_at: datetime
    updated_at: datetime


# Payment Schemas
class PaymentBase(BaseSchema):
    sale_id: UUID
    payment_method: PaymentMethodEnum
    amount: float = Field(..., gt=0)
    payment_date: datetime
    status: PaymentStatusEnum = PaymentStatusEnum.PENDING
    reference_number: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseSchema):
    payment_method: Optional[PaymentMethodEnum] = None
    amount: Optional[float] = Field(None, gt=0)
    payment_date: Optional[datetime] = None
    status: Optional[PaymentStatusEnum] = None
    reference_number: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)


class Payment(PaymentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


# Discount Schemas
class DiscountBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    discount_type: DiscountTypeEnum
    discount_value: float = Field(..., gt=0)
    discount_code: Optional[str] = Field(None, max_length=50)
    min_purchase_amount: Optional[float] = Field(None, ge=0)
    max_discount_amount: Optional[float] = Field(None, ge=0)
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    is_active: bool = True


class DiscountCreate(DiscountBase):
    pass


class DiscountUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    discount_type: Optional[DiscountTypeEnum] = None
    discount_value: Optional[float] = Field(None, gt=0)
    discount_code: Optional[str] = Field(None, max_length=50)
    min_purchase_amount: Optional[float] = Field(None, ge=0)
    max_discount_amount: Optional[float] = Field(None, ge=0)
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    is_active: Optional[bool] = None


class Discount(DiscountBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


# Transaction Report Schemas
class TransactionSummary(BaseSchema):
    total_transactions: int
    total_revenue: float
    average_transaction_value: float
    cash_transactions: int
    card_transactions: int
    digital_transactions: int


class DailySalesReport(BaseSchema):
    date: str
    transaction_summary: TransactionSummary
    top_selling_products: List[dict]
    hourly_breakdown: List[dict]
