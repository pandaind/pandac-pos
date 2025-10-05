from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user
router = APIRouter()
@router.get("/")
def read_discounts(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []
@router.post("/", status_code=201)
def create_discount(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Discount created"}
@router.get("/{discount_id}")
def read_discount(discount_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": discount_id}
@router.put("/{discount_id}")
def update_discount(discount_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": discount_id}
@router.delete("/{discount_id}", status_code=204)
def delete_discount(discount_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None
