from sqlalchemy import Column, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Sale(BaseModel):
    """Sale model."""
    __tablename__ = "sales"

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    discount_id = Column(UUID(as_uuid=True), ForeignKey("discounts.id"), nullable=True)
    product_list = Column(JSON, nullable=False)  # Store product list as JSON
    
    # Relationships
    customer = relationship("Customer", back_populates="sales")
    discount = relationship("Discount")
    transactions = relationship("Transaction", back_populates="sale")


class Transaction(BaseModel):
    """Transaction model."""
    __tablename__ = "transactions"

    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id"), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    payment_type = Column(String(20), nullable=False)  # CreditCard, DebitCard, Cash, Online
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=False)
    
    # Relationships
    sale = relationship("Sale", back_populates="transactions")
    employee = relationship("Employee", back_populates="transactions")
    payment = relationship("Payment", back_populates="transaction")
