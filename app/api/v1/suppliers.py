from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user
router = APIRouter()
@router.get("/")
def read_suppliers(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []
@router.post("/", status_code=201)
def create_supplier(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Supplier created"}
@router.get("/{supplier_id}")
def read_supplier(supplier_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": supplier_id}
@router.put("/{supplier_id}")
def update_supplier(supplier_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": supplier_id}
@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None
