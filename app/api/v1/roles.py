from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import Role, RoleCreate, RoleUpdate
from app.crud.user import role as crud_role
from app.api.deps import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=List[Role])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve all roles.
    """
    roles = crud_role.get_multi(db, skip=skip, limit=limit)
    return roles


@router.post("/", response_model=Role, status_code=status.HTTP_201_CREATED)
def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate,
    current_user = Depends(require_role("admin"))
):
    """
    Create new role.
    Requires admin role.
    """
    role = crud_role.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this name already exists in the system.",
        )
    role = crud_role.create(db, obj_in=role_in)
    return role


@router.get("/{role_id}", response_model=Role)
def read_role(
    role_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get role by ID.
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=Role)
def update_role(
    *,
    db: Session = Depends(get_db),
    role_id: UUID,
    role_in: RoleUpdate,
    current_user = Depends(require_role("admin"))
):
    """
    Update a role.
    Requires admin role.
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role = crud_role.update(db, db_obj=role, obj_in=role_in)
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    *,
    db: Session = Depends(get_db),
    role_id: UUID,
    current_user = Depends(require_role("admin"))
):
    """
    Delete a role.
    Requires admin role.
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    crud_role.remove(db, id=role_id)
    return None
