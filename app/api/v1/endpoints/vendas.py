from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import crud_venda
from app.schemas.venda import VendaCreate, VendaUpdate, VendaResponse
from app.models.vendedor import Vendedor

router = APIRouter()

@router.post("/", response_model=VendaResponse, status_code=status.HTTP_201_CREATED)
def create_venda(
    venda: VendaCreate,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    return crud_venda.create(db, obj_in=venda)

@router.get("/", response_model=List[VendaResponse])
def read_vendas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    return crud_venda.get_multi(db, skip=skip, limit=limit)

@router.get("/{venda_id}", response_model=VendaResponse)
def read_venda(
    venda_id: str,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    venda = crud_venda.get(db, id=venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@router.put("/{venda_id}", response_model=VendaResponse)
def update_venda(
    venda_id: str,
    venda_in: VendaUpdate,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    venda = crud_venda.get(db, id=venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return crud_venda.update(db, db_obj=venda, obj_in=venda_in)

@router.delete("/{venda_id}")
def delete_venda(
    venda_id: str,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    venda = crud_venda.get(db, id=venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    crud_venda.remove(db, id=venda_id)
    return {"message": "Venda deletada com sucesso"} 