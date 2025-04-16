from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import crud_cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.models.vendedor import Vendedor

router = APIRouter()

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    return crud_cliente.create(db, obj_in=cliente)

@router.get("/", response_model=List[ClienteResponse])
def read_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    return crud_cliente.get_multi(db, skip=skip, limit=limit)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def read_cliente(
    cliente_id: str,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    cliente = crud_cliente.get(db, id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: str,
    cliente_in: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    cliente = crud_cliente.get(db, id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud_cliente.update(db, db_obj=cliente, obj_in=cliente_in)

@router.delete("/{cliente_id}")
def delete_cliente(
    cliente_id: str,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user)
):
    cliente = crud_cliente.get(db, id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    crud_cliente.remove(db, id=cliente_id)
    return {"message": "Cliente deletado com sucesso"} 