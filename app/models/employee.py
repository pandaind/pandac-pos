from sqlalchemy import Column, String, Float, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class PaymentMethodEnum(enum.Enum):
    CREDIT_CARD = "CreditCard"
    DEBIT_CARD = "DebitCard"
    CASH = "Cash"
    ONLINE = "Online"


class PaymentStatusEnum(enum.Enum):
    AUTHORIZED = "Authorized"
    CAPTURED = "Captured"
    FAILED = "Failed"


class Payment(BaseModel):
    """Payment model."""
    __tablename__ = "payments"

    amount = Column(Float, nullable=False)
    method = Column(Enum(PaymentMethodEnum), nullable=False)
    status = Column(Enum(PaymentStatusEnum), nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="payment", uselist=False)


class Employee(BaseModel):
    """Employee model."""
    __tablename__ = "employees"

    name = Column(String(100), nullable=False, index=True)
    position = Column(String(50), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    
    # Relationships
    user = relationship("User", back_populates="employee")
    transactions = relationship("Transaction", back_populates="employee")
    pos_sales = relationship("POSSale", back_populates="cashier")


class Supplier(BaseModel):
    """Supplier model."""
    __tablename__ = "suppliers"

    name = Column(String(100), nullable=False, index=True)
    contact_info = Column(String(100), nullable=False)
    product_list = Column(JSON, nullable=True)  # Store product list as JSON
    
    # Relationships
    inventories = relationship("Inventory", back_populates="supplier")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
