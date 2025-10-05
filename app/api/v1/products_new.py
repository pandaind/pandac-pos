from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.crud.product import product as product_crud
from app.models.user import User
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter()


@router.get("/", response_model=List[Product])
def read_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> List[Product]:
    """
    Retrieve products.
    """
    products = product_crud.get_multi(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: ProductCreate,
    current_user: User = Depends(get_current_user),
) -> Product:
    """
    Create new product.
    """
    product = product_crud.create(db=db, obj_in=product_in)
    return product


@router.put("/{product_id}", response_model=Product)
def update_product(
    *,
    db: Session = Depends(get_db),
    product_id: UUID,
    product_in: ProductUpdate,
    current_user: User = Depends(get_current_user),
) -> Product:
    """
    Update a product.
    """
    product = product_crud.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = product_crud.update(db=db, db_obj=product, obj_in=product_in)
    return product


@router.get("/{product_id}", response_model=Product)
def read_product(
    *,
    db: Session = Depends(get_db),
    product_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Product:
    """
    Get product by ID.
    """
    product = product_crud.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}")
def delete_product(
    *,
    db: Session = Depends(get_db),
    product_id: UUID,
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Delete a product.
    """
    product = product_crud.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_crud.remove(db=db, id=product_id)
    return {"message": "Product deleted successfully"}
