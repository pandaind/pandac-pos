from datetime import datetime
from typing import Optional, List
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import BaseSchema


class PaymentMethodEnum(str, Enum):
    CREDIT_CARD = "CreditCard"
    DEBIT_CARD = "DebitCard"
    CASH = "Cash"
    ONLINE = "Online"


class PaymentStatusEnum(str, Enum):
    AUTHORIZED = "Authorized"
    CAPTURED = "Captured"
    FAILED = "Failed"


class TransactionBase(BaseSchema):
    """Base transaction schema."""
    sale_id: UUID
    employee_id: UUID
    payment_type: PaymentMethodEnum
    payment_id: UUID


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    pass


class TransactionUpdate(BaseSchema):
    """Schema for updating a transaction."""
    sale_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    payment_type: Optional[PaymentMethodEnum] = None
    payment_id: Optional[UUID] = None


class Transaction(TransactionBase):
    """Transaction schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class PaymentBase(BaseSchema):
    """Base payment schema."""
    amount: float = Field(..., ge=0)
    method: PaymentMethodEnum
    status: PaymentStatusEnum


class PaymentCreate(PaymentBase):
    """Schema for creating a payment."""
    pass


class PaymentUpdate(BaseSchema):
    """Schema for updating a payment."""
    amount: Optional[float] = Field(None, ge=0)
    method: Optional[PaymentMethodEnum] = None
    status: Optional[PaymentStatusEnum] = None


class Payment(PaymentBase):
    """Payment schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class EmployeeBase(BaseSchema):
    """Base employee schema."""
    name: str = Field(..., min_length=1, max_length=100)
    position: str = Field(..., min_length=1, max_length=50)
    user_id: UUID


class EmployeeCreate(EmployeeBase):
    """Schema for creating an employee."""
    pass


class EmployeeUpdate(BaseSchema):
    """Schema for updating an employee."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[str] = Field(None, min_length=1, max_length=50)
    user_id: Optional[UUID] = None


class Employee(EmployeeBase):
    """Employee schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime
