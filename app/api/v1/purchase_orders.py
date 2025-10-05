from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user
router = APIRouter()
@router.get("/")
def read_purchase_orders(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []
@router.post("/", status_code=201)
def create_purchase_order(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Purchase order created"}
@router.get("/{purchase_order_id}")
def read_purchase_order(purchase_order_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": purchase_order_id}
@router.put("/{purchase_order_id}")
def update_purchase_order(purchase_order_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": purchase_order_id}
@router.delete("/{purchase_order_id}", status_code=204)
def delete_purchase_order(purchase_order_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None
