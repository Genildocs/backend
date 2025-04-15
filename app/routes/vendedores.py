from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, get_password_hash
from app.models import Vendedor
from app.schemas.vendedor import (
    VendedorCreate,
    VendedorUpdate,
    VendedorResponse,
    VendedorList
)

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])

@router.post("", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
async def criar_vendedor(
    vendedor: VendedorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria um novo vendedor"""
    
    # Verifica se já existe vendedor com o email informado
    query = select(Vendedor).where(Vendedor.email == vendedor.email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Cria o vendedor com senha hasheada
    vendedor_data = vendedor.model_dump()
    vendedor_data["senha"] = get_password_hash(vendedor_data["senha"])
    
    db_vendedor = Vendedor(**vendedor_data)
    db.add(db_vendedor)
    await db.commit()
    await db.refresh(db_vendedor)
    
    return db_vendedor


@router.get("", response_model=List[VendedorList])
async def listar_vendedores(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Lista todos os vendedores ativos"""
    
    query = select(Vendedor).where(Vendedor.ativo == True).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{vendedor_id}", response_model=VendedorResponse)
async def obter_vendedor(
    vendedor_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtém um vendedor pelo ID"""
    
    query = select(Vendedor).where(Vendedor.id == vendedor_id)
    result = await db.execute(query)
    vendedor = result.scalar_one_or_none()
    
    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado"
        )
    
    return vendedor


@router.patch("/{vendedor_id}", response_model=VendedorResponse)
async def atualizar_vendedor(
    vendedor_id: str,
    vendedor_update: VendedorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Atualiza um vendedor"""
    
    # Verifica se o vendedor existe
    query = select(Vendedor).where(Vendedor.id == vendedor_id)
    result = await db.execute(query)
    vendedor = result.scalar_one_or_none()
    
    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado"
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = vendedor_update.model_dump(exclude_unset=True)
    
    # Se a senha foi fornecida, faz o hash
    if "senha" in update_data:
        update_data["senha"] = get_password_hash(update_data["senha"])
    
    for field, value in update_data.items():
        setattr(vendedor, field, value)
    
    await db.commit()
    await db.refresh(vendedor)
    
    return vendedor 