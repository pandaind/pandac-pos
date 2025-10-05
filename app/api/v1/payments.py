from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/")
def read_payments(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []

@router.post("/", status_code=201)
def create_payment(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Payment created"}

@router.get("/{payment_id}")
def read_payment(payment_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": payment_id}

@router.put("/{payment_id}")
def update_payment(payment_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": payment_id}

@router.delete("/{payment_id}", status_code=204)
def delete_payment(payment_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None
