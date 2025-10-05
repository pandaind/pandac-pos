from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.core.exceptions import HTTPUnauthorized
from app.crud.user import get_user
from app.models.user import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user.
    """
    token = credentials.credentials
    subject = verify_token(token)
    
    if subject is None:
        raise HTTPUnauthorized("Could not validate credentials")
    
    user = get_user(db, user_id=subject)
    if user is None:
        raise HTTPUnauthorized("User not found")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user.
    """
    # Add any additional checks for active users here
    return current_user


def require_role(required_role: str):
    """
    Factory function to create a dependency that requires a specific role.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.name != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


def require_permissions(required_permissions: list):
    """
    Factory function to create a dependency that requires specific permissions.
    """
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        user_permissions = current_user.role.permissions or []
        if not all(perm in user_permissions for perm in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return permission_checker
