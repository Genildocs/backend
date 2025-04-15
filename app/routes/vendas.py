from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Venda, Item, Cliente, Vendedor
from app.schemas.venda import (
    VendaCreate,
    VendaUpdate,
    VendaResponse,
    VendaList
)

router = APIRouter(prefix="/vendas", tags=["Vendas"])

@router.post("", response_model=VendaResponse, status_code=status.HTTP_201_CREATED)
async def criar_venda(
    venda: VendaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Cria uma nova venda/orçamento"""
    
    # Verifica se o cliente existe
    cliente = await db.get(Cliente, venda.cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    # Verifica se o vendedor existe e está ativo
    vendedor = await db.get(Vendedor, venda.vendedor_id)
    if not vendedor or not vendedor.ativo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado ou inativo"
        )
    
    # Gera o número do documento
    ano_atual = datetime.now().year
    query = select(func.count(Venda.id)).where(
        func.extract('year', Venda.created_at) == ano_atual,
        Venda.tipo == venda.tipo
    )
    result = await db.execute(query)
    count = result.scalar() + 1
    
    numero_documento = f"{venda.tipo[:3]}{ano_atual}{count:04d}"
    
    # Cria a venda
    venda_data = venda.model_dump()
    itens_data = venda_data.pop("itens")
    
    db_venda = Venda(
        **venda_data,
        numero_documento=numero_documento,
        status="PENDING"
    )
    db.add(db_venda)
    await db.flush()  # Para obter o ID da venda
    
    # Cria os itens
    for item_data in itens_data:
        db_item = Item(**item_data, venda_id=db_venda.id)
        db.add(db_item)
    
    await db.commit()
    await db.refresh(db_venda)
    
    return db_venda


@router.get("", response_model=List[VendaList])
async def listar_vendas(
    skip: int = 0,
    limit: int = 100,
    tipo: str = None,
    status: str = None,
    data_inicio: datetime = None,
    data_fim: datetime = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Lista todas as vendas com filtros opcionais"""
    
    query = select(Venda)
    
    if tipo:
        query = query.where(Venda.tipo == tipo)
    if status:
        query = query.where(Venda.status == status)
    if data_inicio:
        query = query.where(Venda.created_at >= data_inicio)
    if data_fim:
        query = query.where(Venda.created_at <= data_fim)
    
    query = query.order_by(Venda.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{venda_id}", response_model=VendaResponse)
async def obter_venda(
    venda_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtém uma venda pelo ID"""
    
    query = select(Venda).where(Venda.id == venda_id)
    result = await db.execute(query)
    venda = result.scalar_one_or_none()
    
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada"
        )
    
    return venda


@router.patch("/{venda_id}/status", response_model=VendaResponse)
async def atualizar_status_venda(
    venda_id: str,
    venda_update: VendaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Atualiza o status de uma venda"""
    
    # Verifica se a venda existe
    query = select(Venda).where(Venda.id == venda_id)
    result = await db.execute(query)
    venda = result.scalar_one_or_none()
    
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada"
        )
    
    # Atualiza o status
    venda.status = venda_update.status
    await db.commit()
    await db.refresh(venda)
    
    return venda 