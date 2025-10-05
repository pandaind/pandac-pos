from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User, Role
from app.schemas.user import UserCreate, UserUpdate, RoleCreate, RoleUpdate
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            password_hash=get_password_hash(obj_in.password),
            role_id=obj_in.role_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_password(self, db: Session, *, db_obj: User, new_password: str) -> User:
        setattr(db_obj, "password_hash", get_password_hash(new_password))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def is_active(self, user: User) -> bool:
        # Add logic to check if user is active
        return True
    
    def is_superuser(self, user: User) -> bool:
        # Add logic to check if user is superuser
        return user.role.name == "admin"


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()


user = CRUDUser(User)
role = CRUDRole(Role)


# Convenience functions
def get_user(db: Session, user_id: UUID) -> Optional[User]:
    return user.get(db=db, id=user_id)


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return user.get_by_username(db=db, username=username)


def create_user(db: Session, user_in: UserCreate) -> User:
    return user.create(db=db, obj_in=user_in)


def get_role(db: Session, role_id: UUID) -> Optional[Role]:
    return role.get(db=db, id=role_id)


def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return role.get_by_name(db=db, name=name)


def create_role(db: Session, role_in: RoleCreate) -> Role:
    return role.create(db=db, obj_in=role_in)
