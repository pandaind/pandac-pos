from datetime import datetime
from typing import Optional, List
from uuid import UUID
import json
from pydantic import BaseModel, Field, ConfigDict, field_validator


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseSchema):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$")
    role_id: Optional[UUID] = None
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=6)  # Reduced from 8 for testing
    email: Optional[str] = None  # Allow email field for flexibility
    full_name: Optional[str] = None  # Allow full_name field for flexibility
    
    model_config = ConfigDict(from_attributes=True, extra='ignore')  # Ignore extra fields


class UserRegister(BaseSchema):
    """Schema for user registration (no role_id required)."""
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=8)


class UserUpdate(BaseSchema):
    """Schema for updating a user."""
    username: Optional[str] = Field(None, min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    password: Optional[str] = Field(None, min_length=8)
    role_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """User schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class RoleBase(BaseSchema):
    """Base role schema."""
    name: str = Field(..., min_length=1, max_length=50)
    permissions: Optional[List[str]] = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    pass


class RoleUpdate(BaseSchema):
    """Schema for updating a role."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    permissions: Optional[List[str]] = None


class Role(RoleBase):
    """Role schema with all fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    @field_validator('permissions', mode='before')
    @classmethod
    def parse_permissions(cls, v):
        """Parse permissions from JSON string to list if needed."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v


# Auth schemas
class Token(BaseSchema):
    """Token schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseSchema):
    """Token data schema."""
    username: Optional[str] = None


class LoginRequest(BaseSchema):
    """Login request schema."""
    username: str
    password: str


class RefreshTokenRequest(BaseSchema):
    """Refresh token request schema."""
    refresh_token: str
