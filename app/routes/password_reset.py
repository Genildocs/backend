from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.password_reset import PasswordResetToken
from app.models.vendedor import Vendedor
from app.core.email import send_password_reset_email
from app.core.exceptions import NotFoundError, ValidationError
from datetime import datetime

router = APIRouter()

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

@router.post("/request-reset")
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Solicita a redefinição de senha.
    Envia um e-mail com o link para redefinição.
    """
    # Busca o vendedor pelo e-mail
    vendedor = db.query(Vendedor).filter(Vendedor.email == request.email).first()
    if not vendedor:
        # Por segurança, não revelamos se o e-mail existe ou não
        return {"message": "Se o e-mail estiver cadastrado, você receberá um link para redefinição de senha."}

    # Cria um novo token
    reset_token = PasswordResetToken.create_token(str(vendedor.id))
    db.add(reset_token)
    db.commit()

    # Envia o e-mail
    if send_password_reset_email(vendedor.email, reset_token.token):
        return {"message": "Se o e-mail estiver cadastrado, você receberá um link para redefinição de senha."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao enviar e-mail de redefinição de senha."
        )

@router.post("/reset")
async def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """
    Redefine a senha usando o token.
    """
    # Busca o token
    token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token
    ).first()

    if not token or not token.is_valid():
        raise ValidationError("Token inválido ou expirado.")

    # Busca o vendedor
    vendedor = db.query(Vendedor).filter(Vendedor.id == token.vendedor_id).first()
    if not vendedor:
        raise NotFoundError("Vendedor")

    # Atualiza a senha
    vendedor.senha = get_password_hash(request.new_password)
    token.used_at = datetime.utcnow()
    
    db.commit()

    return {"message": "Senha redefinida com sucesso."} 