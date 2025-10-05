from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.misc import Settings, Notification
from app.schemas.misc import SettingsCreate, SettingsUpdate, NotificationCreate, NotificationUpdate


class CRUDSettings(CRUDBase[Settings, SettingsCreate, SettingsUpdate]):
    def get_by_key(self, db: Session, *, key: str) -> Optional[Settings]:
        return db.query(Settings).filter(Settings.key == key).first()
    
    def update_setting(self, db: Session, *, key: str, value: str) -> Settings:
        setting = self.get_by_key(db, key=key)
        if setting:
            setting.value = value
            db.commit()
            db.refresh(setting)
        else:
            setting = self.create(db, obj_in=SettingsCreate(key=key, value=value))
        return setting


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def get_by_type(self, db: Session, *, notification_type: str) -> List[Notification]:
        return db.query(Notification).filter(Notification.type == notification_type).all()
    
    def get_recent(self, db: Session, *, limit: int = 10) -> List[Notification]:
        return db.query(Notification).order_by(Notification.timestamp.desc()).limit(limit).all()


# Create instances
settings = CRUDSettings(Settings)
notification = CRUDNotification(Notification)
