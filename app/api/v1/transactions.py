from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/")
def read_transactions(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []

@router.post("/", status_code=201)
def create_transaction(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Transaction created"}

@router.get("/{transaction_id}")
def read_transaction(transaction_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": transaction_id}

@router.put("/{transaction_id}")
def update_transaction(transaction_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": transaction_id}

@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None

@router.get("/{transaction_id}/employee")
def get_transaction_employee(transaction_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"transaction_id": transaction_id}

@router.get("/{transaction_id}/sale")
def get_transaction_sale(transaction_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"transaction_id": transaction_id}

@router.get("/{transaction_id}/payment")
def get_transaction_payment(transaction_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"transaction_id": transaction_id}
