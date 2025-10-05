from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Customer(BaseModel):
    """Customer model."""
    __tablename__ = "customers"

    name = Column(String(100), nullable=False, index=True)
    contact_info = Column(String(100), nullable=False)
    loyalty_points = Column(Integer, nullable=False, default=0)
    
    # Relationships
    sales = relationship("Sale", back_populates="customer")
    pos_sales = relationship("POSSale", back_populates="customer")
    loyalty_programs = relationship("LoyaltyProgram", back_populates="customer")


class LoyaltyProgram(BaseModel):
    """Loyalty program model."""
    __tablename__ = "loyalty_programs"

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    points = Column(Integer, nullable=False, default=0)
    tier = Column(String(20), nullable=False, default="Bronze")  # Bronze, Silver, Gold, Platinum
    
    # Relationships
    customer = relationship("Customer", back_populates="loyalty_programs")
