from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
import logging

from app.core.config import settings
from app.core.database import engine, Base, get_db
from app.api.v1.router import api_router
from app.crud.user import role as crud_role
from app.crud import product as product_crud
from app.schemas.user import RoleCreate
from app.schemas.product import ProductCreate

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize default roles
def init_db():
    """Initialize database with default roles."""
    db = next(get_db())
    try:
        # Create default roles if they don't exist
        if not crud_role.get_by_name(db, name="admin"):
            admin_role = RoleCreate(name="admin", permissions=["*"])
            crud_role.create(db, obj_in=admin_role)
            logger.info("Created admin role")
        
        if not crud_role.get_by_name(db, name="user"):
            user_role = RoleCreate(name="user", permissions=["read"])
            crud_role.create(db, obj_in=user_role)
            logger.info("Created user role")
        
        if not crud_role.get_by_name(db, name="cashier"):
            cashier_role = RoleCreate(name="cashier", permissions=["read", "pos"])
            crud_role.create(db, obj_in=cashier_role)
            logger.info("Created cashier role")
        
        # Database initialization complete
        logger.info("Database initialization completed successfully")
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        db.close()

# Initialize database with default data
init_db()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    API for managing products, inventory, sales, transactions, and employees in a POS system.

    **Versioning Strategy**: This API follows semantic versioning. The version is
    indicated in the base path (`/v1`). Backward-incompatible changes will result
    in a major version increment.
    """,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Pandac.in Support",
        "url": "https://pandac.in",
        "email": "support@pandac.in",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/license/mit",
    },
    terms_of_service="https://pandac.in/terms",
)

# Set up CORS
if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add trusted host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Include API router
app.include_router(api_router, prefix=settings.api_v1_str)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Pandac POS API",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
