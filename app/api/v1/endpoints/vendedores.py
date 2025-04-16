from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import crud_vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate, VendedorResponse
from app.models.vendedor import Vendedor

router = APIRouter()

@router.post("/", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
def create_vendedor(
    vendedor: VendedorCreate,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    return crud_vendedor.create(db, obj_in=vendedor)

@router.get("/", response_model=List[VendedorResponse])
def read_vendedores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    return crud_vendedor.get_multi(db, skip=skip, limit=limit)

@router.get("/{vendedor_id}", response_model=VendedorResponse)
def read_vendedor(
    vendedor_id: str,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    vendedor = crud_vendedor.get(db, id=vendedor_id)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return vendedor

@router.put("/{vendedor_id}", response_model=VendedorResponse)
def update_vendedor(
    vendedor_id: str,
    vendedor_in: VendedorUpdate,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    vendedor = crud_vendedor.get(db, id=vendedor_id)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return crud_vendedor.update(db, db_obj=vendedor, obj_in=vendedor_in)

@router.delete("/{vendedor_id}")
def delete_vendedor(
    vendedor_id: str,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    vendedor = crud_vendedor.get(db, id=vendedor_id)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    crud_vendedor.remove(db, id=vendedor_id)
    return {"message": "Vendedor deletado com sucesso"} 