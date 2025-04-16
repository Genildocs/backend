from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationResponse, NotificationUpdate
from app.core.security import get_current_user
from app.models.vendedor import Vendedor
from app.core.errors import NotFoundError
from app.core.permissions import require_permission

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
@require_permission("create_notifications")
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    """Cria uma nova notificação para um vendedor"""
    db_notification = Notification(
        **notification.dict(),
        vendedor_id=current_user.id
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/", response_model=List[NotificationResponse])
@require_permission("view_notifications")
async def get_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    """Lista todas as notificações do vendedor"""
    notifications = db.query(Notification)\
        .filter(Notification.vendedor_id == current_user.id)\
        .order_by(Notification.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return notifications

@router.get("/unread", response_model=List[NotificationResponse])
@require_permission("view_notifications")
async def get_unread_notifications(
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    """Lista todas as notificações não lidas do vendedor"""
    notifications = db.query(Notification)\
        .filter(
            Notification.vendedor_id == current_user.id,
            Notification.is_read == False
        )\
        .order_by(Notification.created_at.desc())\
        .all()
    return notifications

@router.put("/{notification_id}", response_model=NotificationResponse)
@require_permission("edit_notifications")
async def update_notification(
    notification_id: str,
    notification: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    """Atualiza uma notificação"""
    db_notification = db.query(Notification)\
        .filter(
            Notification.id == notification_id,
            Notification.vendedor_id == current_user.id
        )\
        .first()
    
    if not db_notification:
        raise NotFoundError("Notificação não encontrada")
    
    for key, value in notification.dict(exclude_unset=True).items():
        setattr(db_notification, key, value)
    
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.delete("/{notification_id}")
@require_permission("delete_notifications")
async def delete_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    """Deleta uma notificação"""
    db_notification = db.query(Notification)\
        .filter(
            Notification.id == notification_id,
            Notification.vendedor_id == current_user.id
        )\
        .first()
    
    if not db_notification:
        raise NotFoundError("Notificação não encontrada")
    
    db.delete(db_notification)
    db.commit()
    return {"message": "Notificação deletada com sucesso"} 