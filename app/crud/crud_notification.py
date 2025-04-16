from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def create_notification(
        self, db: Session, *, obj_in: NotificationCreate, vendedor_id: str
    ) -> Notification:
        db_obj = Notification(
            title=obj_in.title,
            message=obj_in.message,
            type=obj_in.type,
            vendedor_id=vendedor_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_notifications_by_vendedor(
        self, db: Session, *, vendedor_id: str, skip: int = 0, limit: int = 100, is_read: Optional[bool] = None
    ) -> List[Notification]:
        query = db.query(self.model).filter(Notification.vendedor_id == vendedor_id)
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        return query.offset(skip).limit(limit).all()

    def mark_as_read(self, db: Session, *, id: str) -> Notification:
        db_obj = db.query(self.model).filter(Notification.id == id).first()
        if db_obj:
            db_obj.is_read = True
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

crud_notification = CRUDNotification(Notification) 