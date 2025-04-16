from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.schemas.notification import Notification, NotificationCreate, NotificationUpdate

router = APIRouter()

@router.get("/", response_model=List[Notification])
def get_notifications(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_read: Optional[bool] = None,
    current_vendedor: schemas.Vendedor = Depends(deps.get_current_vendedor)
):
    """
    Listar notificações do vendedor
    """
    notifications = crud.notification.get_notifications_by_vendedor(
        db=db,
        vendedor_id=current_vendedor.id,
        skip=skip,
        limit=limit,
        is_read=is_read
    )
    return notifications

@router.post("/", response_model=Notification)
def create_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_in: NotificationCreate,
    current_vendedor: schemas.Vendedor = Depends(deps.get_current_vendedor)
):
    """
    Criar nova notificação
    """
    notification = crud.notification.create_notification(
        db=db,
        obj_in=notification_in,
        vendedor_id=current_vendedor.id
    )
    return notification

@router.put("/{notification_id}", response_model=Notification)
def mark_notification_as_read(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: str,
    current_vendedor: schemas.Vendedor = Depends(deps.get_current_vendedor)
):
    """
    Marcar notificação como lida
    """
    notification = crud.notification.mark_as_read(
        db=db,
        notification_id=notification_id,
        vendedor_id=current_vendedor.id
    )
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    return notification 