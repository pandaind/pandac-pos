from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_password, verify_token
from app.schemas.user import Token, LoginRequest, RefreshTokenRequest, User, UserRegister, UserCreate
from app.crud.user import get_user_by_username, user as crud_user, role as crud_role
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=Token, summary="User login")
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    User login endpoint.
    
    Returns access and refresh tokens upon successful authentication.
    """
    user = get_user_by_username(db, username=login_data.username)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED, summary="User registration")
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    User registration endpoint.
    
    Allows new users to register without authentication.
    Creates a new user account with default 'user' role and returns user information.
    """
    # Check if username already exists
    existing_user = get_user_by_username(db, username=user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Get default 'user' role
    default_role = crud_role.get_by_name(db, name="user")
    if not default_role:
        # If 'user' role doesn't exist, create it
        from app.schemas.user import RoleCreate
        role_data = RoleCreate(name="user", permissions=["read"])
        default_role = crud_role.create(db, obj_in=role_data)
    
    # Create UserCreate object with default role
    user_create_data = UserCreate(
        username=user_data.username,
        password=user_data.password,
        role_id=default_role.id
    )
    
    # Create new user
    user = crud_user.create(db, obj_in=user_create_data)
    return user


@router.post("/logout", summary="User logout")
async def logout():
    """
    User logout endpoint.
    
    In a production environment, you would typically blacklist the token.
    """
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=Token, summary="Refresh access token")
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    from uuid import UUID
    
    subject = verify_token(refresh_data.refresh_token)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify user still exists (subject is user_id UUID)
    try:
        user_id = UUID(subject)
        user = crud_user.get(db, id=user_id)
    except (ValueError, AttributeError):
        user = None
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    new_refresh_token = create_refresh_token(subject=user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )
