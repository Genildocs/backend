from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import crud_vendedor
from app.schemas.vendedor import VendedorUpdate
from app.models.vendedor import Vendedor
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/request-reset")
def request_password_reset(
    email: str,
    db: Session = Depends(get_db)
) -> Any:
    vendedor = crud_vendedor.get_by_email(db, email=email)
    if not vendedor:
        raise HTTPException(
            status_code=404,
            detail="Email não encontrado"
        )
    # Aqui você implementaria a lógica de envio de email
    return {"message": "Email de recuperação enviado"}

@router.post("/reset")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
) -> Any:
    # Aqui você implementaria a validação do token
    # Por enquanto, vamos apenas atualizar a senha
    vendedor = crud_vendedor.get_by_reset_token(db, token=token)
    if not vendedor:
        raise HTTPException(
            status_code=400,
            detail="Token inválido"
        )
    
    vendedor_in = VendedorUpdate(senha=new_password)
    vendedor_in.senha = get_password_hash(new_password)
    crud_vendedor.update(db, db_obj=vendedor, obj_in=vendedor_in)
    
    return {"message": "Senha atualizada com sucesso"} 