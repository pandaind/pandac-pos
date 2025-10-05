from typing import Optional, List
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.crud.base import CRUDBase
from app.models.employee import Supplier
from app.models.misc import PurchaseOrder
from app.schemas.misc import (
    SupplierCreate, SupplierUpdate, 
    PurchaseOrderCreate, PurchaseOrderUpdate
)


class CRUDSupplier(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    def get_by_contact(self, db: Session, *, contact_info: str) -> Optional[Supplier]:
        return db.query(Supplier).filter(Supplier.contact_info == contact_info).first()
    
    def search_by_name(self, db: Session, *, name: str) -> List[Supplier]:
        return db.query(Supplier).filter(
            Supplier.name.ilike(f"%{name}%")
        ).all()


class CRUDPurchaseOrder(CRUDBase[PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate]):
    def get_by_supplier(self, db: Session, *, supplier_id: UUID) -> List[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(
            PurchaseOrder.supplier_id == supplier_id
        ).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(PurchaseOrder.status == status).all()
    
    def get_pending_orders(self, db: Session) -> List[PurchaseOrder]:
        return self.get_by_status(db, status="Pending")
    
    def get_by_date_range(
        self, 
        db: Session, 
        *, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(
            and_(
                PurchaseOrder.order_date >= start_date,
                PurchaseOrder.order_date <= end_date
            )
        ).all()
    
    def update_status(
        self, 
        db: Session, 
        *, 
        order_id: UUID, 
        status: str
    ) -> PurchaseOrder:
        order = self.get(db, id=order_id)
        if order:
            order.status = status
            if status == "Delivered":
                order.expected_delivery_date = datetime.now()
            db.commit()
            db.refresh(order)
        return order


# Create instances
supplier = CRUDSupplier(Supplier)
purchase_order = CRUDPurchaseOrder(PurchaseOrder)
