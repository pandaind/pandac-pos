from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user
router = APIRouter()
@router.get("/")
def read_settings(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []
@router.post("/", status_code=201)
def create_setting(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Setting created"}
@router.get("/{setting_id}")
def read_setting(setting_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": setting_id}
@router.put("/{setting_id}")
def update_setting(setting_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"id": setting_id}
@router.delete("/{setting_id}", status_code=204)
def delete_setting(setting_id: str, db = Depends(get_db), current_user = Depends(get_current_user)):
    return None
