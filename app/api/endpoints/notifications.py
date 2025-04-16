from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.crud import crud_notification
from app.schemas.notification import Notification, NotificationCreate, NotificationUpdate
from app.api.deps import get_db, get_current_vendedor

router = APIRouter()

@router.post("/", response_model=Notification)
def create_notification(
    *,
    db: Session = Depends(get_db),
    notification_in: NotificationCreate,
    current_vendedor = Depends(get_current_vendedor)
):
    """
    Criar nova notificação
    """
    notification = crud_notification.create_notification(
        db=db, 
        obj_in=notification_in,
        vendedor_id=current_vendedor.id
    )
    return notification

@router.get("/", response_model=List[Notification])
def read_notifications(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    is_read: Optional[bool] = None,
    current_vendedor = Depends(get_current_vendedor)
):
    """
    Listar notificações do vendedor
    """
    notifications = crud_notification.get_notifications_by_vendedor(
        db=db,
        vendedor_id=current_vendedor.id,
        skip=skip,
        limit=limit,
        is_read=is_read
    )
    return notifications

@router.get("/{notification_id}", response_model=Notification)
def read_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_vendedor = Depends(get_current_vendedor)
):
    """
    Obter notificação por ID
    """
    notification = crud_notification.get_notification(db=db, id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    if notification.vendedor_id != current_vendedor.id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    return notification

@router.put("/{notification_id}", response_model=Notification)
def update_notification(
    *,
    db: Session = Depends(get_db),
    notification_id: str,
    notification_in: NotificationUpdate,
    current_vendedor = Depends(get_current_vendedor)
):
    """
    Atualizar notificação
    """
    notification = crud_notification.get_notification(db=db, id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    if notification.vendedor_id != current_vendedor.id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    notification = crud_notification.update_notification(
        db=db, db_obj=notification, obj_in=notification_in
    )
    return notification

@router.delete("/{notification_id}", response_model=Notification)
def delete_notification(
    *,
    db: Session = Depends(get_db),
    notification_id: str,
    current_vendedor = Depends(get_current_vendedor)
):
    """
    Deletar notificação
    """
    notification = crud_notification.get_notification(db=db, id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    if notification.vendedor_id != current_vendedor.id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    notification = crud_notification.delete_notification(db=db, id=notification_id)
    return notification

@router.post("/{notification_id}/read", response_model=Notification)
def mark_notification_as_read(
    *,
    db: Session = Depends(get_db),
    notification_id: str,
    current_vendedor = Depends(get_current_vendedor)
):
    """
    Marcar notificação como lida
    """
    notification = crud_notification.get_notification(db=db, id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    if notification.vendedor_id != current_vendedor.id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    notification = crud_notification.mark_as_read(db=db, id=notification_id)
    return notification 