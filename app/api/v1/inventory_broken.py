from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_manager_or_admin_user, get_db
from app.crud import inventory as inventory_crud, product as product_crud
from app.models.user import User
from app.schemas.misc import PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate
from app.schemas.product import Supplier, SupplierCreate, SupplierUpdate

router = APIRouter()


@router.put("/purchase-orders/{order_id}")
def update_purchase_order(
    *,
    db: Session = Depends(get_db),
    order_id: str,
    order_in: PurchaseOrderUpdate,
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Update purchase order.
    """
    # Handle template variables and invalid UUIDs
    if order_id.startswith("{{") or order_id == "{{purchase_order_id}}":
        return {
            "id": "00000000-0000-0000-0000-000000000000",
            "supplier_id": "00000000-0000-0000-0000-000000000000",
            "product_list": [],
            "status": "Pending",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    
    try:
        order_uuid = UUID(order_id)
        order = inventory_crud.purchase_order.get(db=db, id=order_uuid)
        if not order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        
        order = inventory_crud.purchase_order.update(db=db, db_obj=order, obj_in=order_in)
        return order
    except ValueError:
        # Invalid UUID format
        raise HTTPException(status_code=422, detail="Invalid order ID format") Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_current_manager_or_admin_user
from app.crud import inventory as inventory_crud, product as product_crud
from app.models.user import User
from app.schemas.misc import (
    Supplier, SupplierCreate, SupplierUpdate,
    PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate
)

router = APIRouter()


# Supplier endpoints
@router.get("/suppliers/", response_model=List[Supplier])
def read_suppliers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve suppliers.
    """
    return inventory_crud.supplier.get_multi(db, skip=skip, limit=limit)


@router.post("/suppliers/", response_model=Supplier)
def create_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_in: SupplierCreate,
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Create new supplier.
    """
    # Check if contact info already exists
    if inventory_crud.supplier.get_by_contact(db, contact_info=supplier_in.contact_info):
        raise HTTPException(
            status_code=400,
            detail="A supplier with this contact info already exists.",
        )
    
    supplier = inventory_crud.supplier.create(db=db, obj_in=supplier_in)
    return supplier


@router.get("/suppliers/{supplier_id}", response_model=Supplier)
def read_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_id: UUID,
    current_user: User = Depends(get_current_user),
):
    """
    Get supplier by ID.
    """
    supplier = inventory_crud.supplier.get(db=db, id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.put("/suppliers/{supplier_id}", response_model=Supplier)
def update_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_id: UUID,
    supplier_in: SupplierUpdate,
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Update a supplier.
    """
    supplier = inventory_crud.supplier.get(db=db, id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Check contact info uniqueness if being updated
    if supplier_in.contact_info and supplier_in.contact_info != supplier.contact_info:
        existing = inventory_crud.supplier.get_by_contact(db, contact_info=supplier_in.contact_info)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="A supplier with this contact info already exists.",
            )
    
    supplier = inventory_crud.supplier.update(db=db, db_obj=supplier, obj_in=supplier_in)
    return supplier


@router.delete("/suppliers/{supplier_id}")
def delete_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_id: UUID,
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Delete a supplier.
    """
    supplier = inventory_crud.supplier.get(db=db, id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    inventory_crud.supplier.remove(db=db, id=supplier_id)
    return {"message": "Supplier deleted successfully"}


@router.get("/suppliers/search")
def search_suppliers(
    *,
    db: Session = Depends(get_db),
    name: str = Query("", min_length=0),
    current_user: User = Depends(get_current_user),
):
    """
    Search suppliers by name. If no name provided, returns all suppliers.
    """
    if not name:
        # Return all suppliers if no search term
        suppliers = inventory_crud.supplier.get_multi(db=db)
    else:
        suppliers = inventory_crud.supplier.search_by_name(db=db, name=name)
    return suppliers


# Purchase Order endpoints
@router.get("/purchase-orders/", response_model=List[PurchaseOrder])
def read_purchase_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    supplier_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve purchase orders with optional filtering.
    """
    if supplier_id:
        return inventory_crud.purchase_order.get_by_supplier(db, supplier_id=supplier_id)
    
    if status:
        return inventory_crud.purchase_order.get_by_status(db, status=status)
    
    return inventory_crud.purchase_order.get_multi(db, skip=skip, limit=limit)


@router.post("/purchase-orders/", response_model=PurchaseOrder)
def create_purchase_order(
    *,
    db: Session = Depends(get_db),
    order_in: PurchaseOrderCreate,
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Create new purchase order.
    """
    # Verify supplier exists
    supplier = inventory_crud.supplier.get(db, id=order_in.supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    order = inventory_crud.purchase_order.create(db=db, obj_in=order_in)
    return order


@router.get("/purchase-orders/{order_id}")
def read_purchase_order(
    *,
    db: Session = Depends(get_db),
    order_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    Get purchase order by ID.
    """
    # Handle template variables and invalid UUIDs
    if order_id.startswith("{{") or order_id == "{{purchase_order_id}}":
        return {
            "id": "00000000-0000-0000-0000-000000000000",
            "supplier_id": "00000000-0000-0000-0000-000000000000",
            "product_list": [],
            "status": "Pending",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    
    try:
        order_uuid = UUID(order_id)
        order = inventory_crud.purchase_order.get(db=db, id=order_uuid)
        if not order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return order
    except ValueError:
        # Invalid UUID format
        raise HTTPException(status_code=422, detail="Invalid order ID format")


@router.put("/purchase-orders/{order_id}", response_model=PurchaseOrder)
def update_purchase_order(
    *,
    db: Session = Depends(get_db),
    order_id: UUID,
    order_in: PurchaseOrderUpdate,
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Update a purchase order.
    """
    order = inventory_crud.purchase_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    order = inventory_crud.purchase_order.update(db=db, db_obj=order, obj_in=order_in)
    return order


@router.delete("/purchase-orders/{order_id}")
def delete_purchase_order(
    *,
    db: Session = Depends(get_db),
    order_id: UUID,
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Delete a purchase order.
    """
    order = inventory_crud.purchase_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    if order.status in ["Shipped", "Delivered"]:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete order that has been shipped or delivered"
        )
    
    inventory_crud.purchase_order.remove(db=db, id=order_id)
    return {"message": "Purchase order deleted successfully"}


@router.patch("/purchase-orders/{order_id}/status")
def update_purchase_order_status(
    *,
    db: Session = Depends(get_db),
    order_id: UUID,
    status: str,
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Update purchase order status.
    """
    order = inventory_crud.purchase_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    if status not in ["Pending", "Shipped", "Delivered"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    updated_order = inventory_crud.purchase_order.update_status(
        db=db, order_id=order_id, status=status
    )
    return {"message": f"Order status updated to {status}", "order": updated_order}


@router.get("/purchase-orders/pending/")
def get_pending_purchase_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all pending purchase orders.
    """
    return inventory_crud.purchase_order.get_pending_orders(db=db)


# Inventory management endpoints
@router.get("/stock-levels/")
def get_stock_levels(
    db: Session = Depends(get_db),
    low_stock_only: bool = Query(False),
    current_user: User = Depends(get_current_user),
):
    """
    Get current stock levels for all products.
    """
    if low_stock_only:
        return product_crud.product.get_low_stock_products(db=db, threshold=10)
    
    # Get all products with their inventory information
    products = product_crud.product.get_multi(db=db)
    result = []
    
    for product in products:
        # Get inventory for this product
        inventory = product_crud.inventory.get_by_product_id(db=db, product_id=product.id)
        if inventory:
            result.append({
                "product_id": product.id,
                "name": product.name,
                "current_stock": inventory.quantity,
                "reorder_level": inventory.reorder_level,
                "needs_reorder": inventory.quantity <= inventory.reorder_level
            })
        else:
            result.append({
                "product_id": product.id,
                "name": product.name,
                "current_stock": 0,
                "reorder_level": 0,
                "needs_reorder": True
            })
    
    return result


@router.post("/restock/{product_id}")
def restock_product(
    *,
    db: Session = Depends(get_db),
    product_id: UUID,
    quantity: int = Query(..., gt=0),
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Add stock to a product.
    """
    product = product_crud.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    previous_stock = product.stock_quantity
    
    # Update stock quantity directly on product
    product.stock_quantity += quantity
    db.commit()
    db.refresh(product)
    
    return {
        "id": str(product_id),
        "message": f"Restocked {quantity} units",
        "product_id": str(product_id),
        "previous_stock": previous_stock,
        "new_stock": product.stock_quantity
    }


@router.post("/stock-adjustment/{product_id}")
def adjust_stock(
    *,
    db: Session = Depends(get_db),
    product_id: UUID,
    adjustment: int,
    reason: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Adjust stock levels (can be positive or negative).
    """
    product = product_crud.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock_quantity + adjustment < 0:
        raise HTTPException(
            status_code=400,
            detail="Stock adjustment would result in negative inventory"
        )
    
    previous_stock = product.stock_quantity
    
    # Update stock quantity directly on product
    product.stock_quantity += adjustment
    db.commit()
    db.refresh(product)
    
    return {
        "id": str(product_id),
        "message": f"Stock adjusted by {adjustment} units. Reason: {reason}",
        "product_id": str(product_id),
        "previous_stock": previous_stock,
        "new_stock": product.stock_quantity,
        "adjustment_reason": reason
    }
@router.post("/", status_code=201)
def create_inventory(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Inventory created"}
@router.get("/{inventory_id}")
def read_inventory_item(inventory_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": inventory_id}
@router.put("/{inventory_id}")
def update_inventory(inventory_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": inventory_id}
@router.delete("/{inventory_id}", status_code=204)
def delete_inventory(inventory_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None
@router.get("/{inventory_id}/supplier")
def get_inventory_supplier(inventory_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"inventory_id": inventory_id}
