from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.crud.customer import customer as customer_crud
from app.models.user import User
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()


@router.get("/", response_model=List[Customer])
def read_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> List[Customer]:
    """
    Retrieve customers.
    """
    customers = customer_crud.get_multi(db, skip=skip, limit=limit)
    return customers


@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(
    *,
    db: Session = Depends(get_db),
    customer_in: CustomerCreate,
    current_user: User = Depends(get_current_user),
) -> Customer:
    """
    Create new customer.
    """
    customer = customer_crud.create(db=db, obj_in=customer_in)
    return customer


@router.put("/{customer_id}", response_model=Customer)
def update_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: UUID,
    customer_in: CustomerUpdate,
    current_user: User = Depends(get_current_user),
) -> Customer:
    """
    Update a customer.
    """
    customer = customer_crud.get(db=db, id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer = customer_crud.update(db=db, db_obj=customer, obj_in=customer_in)
    return customer


@router.get("/{customer_id}", response_model=Customer)
def read_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Customer:
    """
    Get customer by ID.
    """
    customer = customer_crud.get(db=db, id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}")
def delete_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: UUID,
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Delete a customer.
    """
    customer = customer_crud.get(db=db, id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_crud.remove(db=db, id=customer_id)
    return {"message": "Customer deleted successfully"}
