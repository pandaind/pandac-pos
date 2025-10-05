from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user
router = APIRouter()
@router.get("/")
def read_loyalty_programs(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []
@router.post("/", status_code=201)
def create_loyalty_program(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Loyalty program created"}
@router.get("/{program_id}")
def read_loyalty_program(program_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": program_id}
@router.put("/{program_id}")
def update_loyalty_program(program_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": program_id}
@router.delete("/{program_id}", status_code=204)
def delete_loyalty_program(program_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None
