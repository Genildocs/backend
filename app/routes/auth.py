from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models import Vendedor
from app.schemas.vendedor import VendedorAuth
from datetime import timedelta
import os

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
async def login(
    auth_data: VendedorAuth,
    db: AsyncSession = Depends(get_db)
):
    """Autenticação de vendedor com email e senha"""
    
    # Busca o vendedor pelo email
    query = select(Vendedor).where(Vendedor.email == auth_data.email)
    result = await db.execute(query)
    vendedor = result.scalar_one_or_none()
    
    if not vendedor or not verify_password(auth_data.senha, vendedor.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    if not vendedor.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo"
        )
    
    # Cria o token JWT
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    )
    
    access_token = create_access_token(
        data={"sub": str(vendedor.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "vendedor": {
            "id": vendedor.id,
            "nome": vendedor.nome,
            "email": vendedor.email
        }
    } 