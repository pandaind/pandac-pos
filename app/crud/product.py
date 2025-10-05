from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.product import Product, Inventory
from app.models.employee import Supplier
from app.models.misc import PurchaseOrder, Discount
from app.schemas.product import ProductCreate, ProductUpdate, InventoryCreate, InventoryUpdate
from app.schemas.misc import SupplierCreate, SupplierUpdate, PurchaseOrderCreate, PurchaseOrderUpdate, DiscountCreate, DiscountUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Product]:
        return db.query(Product).filter(Product.name == name).first()
    
    def get_by_category(self, db: Session, *, category: str) -> List[Product]:
        return db.query(Product).filter(Product.category == category).all()
    
    def search_products(self, db: Session, *, search: str) -> List[Product]:
        return db.query(Product).filter(
            Product.name.ilike(f"%{search}%") | 
            Product.description.ilike(f"%{search}%")
        ).all()
    
    def get_low_stock_products(self, db: Session, *, threshold: int = 10) -> List[Product]:
        """Get products with low stock levels"""
        # Join with inventory table to check stock levels
        return db.query(Product).join(Inventory).filter(
            Inventory.quantity <= threshold
        ).all()


class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    def get_by_product_id(self, db: Session, *, product_id: UUID) -> Optional[Inventory]:
        return db.query(Inventory).filter(Inventory.product_id == product_id).first()
    
    def get_low_stock(self, db: Session) -> List[Inventory]:
        return db.query(Inventory).filter(Inventory.quantity <= Inventory.reorder_level).all()
    
    def update_stock(self, db: Session, *, product_id: UUID, quantity_change: int) -> Optional[Inventory]:
        inventory = self.get_by_product_id(db, product_id=product_id)
        if inventory:
            inventory.quantity += quantity_change
            db.commit()
            db.refresh(inventory)
        return inventory


class CRUDSupplier(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Supplier]:
        return db.query(Supplier).filter(Supplier.name == name).first()


class CRUDPurchaseOrder(CRUDBase[PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate]):
    def get_by_supplier(self, db: Session, *, supplier_id: UUID) -> List[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(PurchaseOrder.supplier_id == supplier_id).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(PurchaseOrder.status == status).all()


class CRUDDiscount(CRUDBase[Discount, DiscountCreate, DiscountUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Discount]:
        return db.query(Discount).filter(Discount.name == name).first()
    
    def get_active_discounts(self, db: Session) -> List[Discount]:
        # In a real application, you might have start/end dates for discounts
        return db.query(Discount).all()


# Create instances
product = CRUDProduct(Product)
inventory = CRUDInventory(Inventory)
supplier = CRUDSupplier(Supplier)
purchase_order = CRUDPurchaseOrder(PurchaseOrder)
discount = CRUDDiscount(Discount)
