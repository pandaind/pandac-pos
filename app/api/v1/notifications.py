from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.api.deps import get_current_user
router = APIRouter()
@router.get("/")
def read_notifications(db = Depends(get_db), current_user = Depends(get_current_user)):
    return []
@router.post("/", status_code=201)
def create_notification(db = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Notification created"}
