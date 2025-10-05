from sqlalchemy import Column, String, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    """User model."""
    __tablename__ = "users"

    username = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="users")
    employee = relationship("Employee", back_populates="user", uselist=False)


class Role(BaseModel):
    """Role model."""
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False)
    permissions = Column(JSON, nullable=True)  # JSON array of permissions
    
    # Relationships
    users = relationship("User", back_populates="role")
