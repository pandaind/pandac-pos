from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user
router = APIRouter()
@router.get("/")
def read_employees(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []
@router.post("/", status_code=201)
def create_employee(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Employee created"}
@router.get("/{employee_id}")
def read_employee(employee_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": employee_id}
@router.put("/{employee_id}")
def update_employee(employee_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": employee_id}
@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None
@router.get("/{employee_id}/transactions")
def get_employee_transactions(employee_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return []
