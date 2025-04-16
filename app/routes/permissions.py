from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.permission import Permission
from app.models.vendedor import Vendedor
from app.core.permissions import require_permission
from app.core.security import get_current_user
from app.core.exceptions import NotFoundError

router = APIRouter()

class PermissionBase(BaseModel):
    name: str
    description: str
    module: str

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: str
    is_active: bool

    class Config:
        from_attributes = True

class VendedorPermissionUpdate(BaseModel):
    permission_ids: List[str]

@router.post("/", response_model=PermissionResponse)
@require_permission("edit_configuracoes")
async def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db)
):
    """Cria uma nova permissão."""
    db_permission = Permission(
        name=permission.name,
        description=permission.description,
        module=permission.module
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.get("/", response_model=List[PermissionResponse])
@require_permission("view_configuracoes")
async def list_permissions(
    db: Session = Depends(get_db)
):
    """Lista todas as permissões."""
    return db.query(Permission).all()

@router.get("/vendedor/{vendedor_id}", response_model=List[PermissionResponse])
@require_permission("view_configuracoes")
async def get_vendedor_permissions(
    vendedor_id: str,
    db: Session = Depends(get_db)
):
    """Obtém as permissões de um vendedor."""
    vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    if not vendedor:
        raise NotFoundError("Vendedor")
    return vendedor.permissions

@router.put("/vendedor/{vendedor_id}")
@require_permission("edit_configuracoes")
async def update_vendedor_permissions(
    vendedor_id: str,
    update: VendedorPermissionUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza as permissões de um vendedor."""
    vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
    if not vendedor:
        raise NotFoundError("Vendedor")
    
    # Remove todas as permissões atuais
    vendedor.permissions = []
    
    # Adiciona as novas permissões
    permissions = db.query(Permission).filter(Permission.id.in_(update.permission_ids)).all()
    vendedor.permissions = permissions
    
    db.commit()
    return {"message": "Permissões atualizadas com sucesso"} 