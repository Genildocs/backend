from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Cliente
from app.schemas.cliente import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteList
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    cliente: ClienteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria um novo cliente"""
    
    # Verifica se já existe cliente com o CPF informado
    query = select(Cliente).where(Cliente.cpf == cliente.cpf)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado"
        )
    
    # Cria o cliente
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    
    return db_cliente


@router.get("", response_model=List[ClienteList])
async def listar_clientes(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Lista todos os clientes com paginação e busca opcional"""
    
    query = select(Cliente)
    
    if search:
        search = f"%{search}%"
        query = query.where(
            (Cliente.nome.ilike(search)) |
            (Cliente.cpf.ilike(search)) |
            (Cliente.telefone.ilike(search))
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obter_cliente(
    cliente_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtém um cliente pelo ID"""
    
    query = select(Cliente).where(Cliente.id == cliente_id)
    result = await db.execute(query)
    cliente = result.scalar_one_or_none()
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(
    cliente_id: str,
    cliente_update: ClienteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Atualiza um cliente"""
    
    # Verifica se o cliente existe
    query = select(Cliente).where(Cliente.id == cliente_id)
    result = await db.execute(query)
    cliente = result.scalar_one_or_none()
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = cliente_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cliente, field, value)
    
    await db.commit()
    await db.refresh(cliente)
    
    return cliente 