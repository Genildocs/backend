from typing import List, Optional
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.base import CRUDBase

class CRUDNotification(CRUDBase[models.Notification, schemas.NotificationCreate, schemas.NotificationUpdate]):
    def create_notification(
        self,
        db: Session,
        *,
        obj_in: schemas.NotificationCreate,
        vendedor_id: str
    ) -> models.Notification:
        db_obj = self.model(
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
        self,
        db: Session,
        *,
        vendedor_id: str,
        skip: int = 0,
        limit: int = 100,
        is_read: Optional[bool] = None
    ) -> List[models.Notification]:
        query = db.query(self.model).filter(self.model.vendedor_id == vendedor_id)
        if is_read is not None:
            query = query.filter(self.model.is_read == is_read)
        return query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

    def mark_as_read(
        self,
        db: Session,
        *,
        notification_id: str,
        vendedor_id: str
    ) -> Optional[models.Notification]:
        notification = db.query(self.model).filter(
            self.model.id == notification_id,
            self.model.vendedor_id == vendedor_id
        ).first()
        if notification:
            notification.is_read = True
            db.add(notification)
            db.commit()
            db.refresh(notification)
        return notification

notification = CRUDNotification(models.Notification) 