from sqlalchemy import Column, String, Float, ForeignKey, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class POSSale(BaseModel):
    """POS Sale model."""
    __tablename__ = "pos_sales"

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    cashier_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    discount_id = Column(UUID(as_uuid=True), ForeignKey("discounts.id"), nullable=True)
    
    # Relationships (use string references to avoid circular imports)
    customer = relationship("Customer", back_populates="pos_sales")
    cashier = relationship("Employee", back_populates="pos_sales")
    sale_items = relationship("POSSaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = relationship("POSPayment", back_populates="sale", cascade="all, delete-orphan")


class POSSaleItem(BaseModel):
    """POS Sale item model."""
    __tablename__ = "pos_sale_items"

    sale_id = Column(UUID(as_uuid=True), ForeignKey("pos_sales.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Relationships (use string references to avoid circular imports)
    sale = relationship("POSSale", back_populates="sale_items")
    product = relationship("Product")


class PaymentMethodEnum(enum.Enum):
    CASH = "Cash"
    CREDIT_CARD = "CreditCard"
    DEBIT_CARD = "DebitCard"
    DIGITAL_WALLET = "DigitalWallet"
    BANK_TRANSFER = "BankTransfer"


class PaymentStatusEnum(enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class POSPayment(BaseModel):
    """POS Payment model."""
    __tablename__ = "pos_payments"

    sale_id = Column(UUID(as_uuid=True), ForeignKey("pos_sales.id"), nullable=False)
    payment_method = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="Completed")
    transaction_id = Column(String(100), nullable=True)
    
    # Relationships (use string references to avoid circular imports)
    sale = relationship("POSSale", back_populates="payments")


class POSDiscount(BaseModel):
    """POS Discount model."""
    __tablename__ = "pos_discounts"

    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # percentage, fixed_amount
    value = Column(Float, nullable=False)
    applicable_products = Column(JSON, nullable=True)  # Store product IDs as JSON array
