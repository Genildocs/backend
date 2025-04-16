from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class CRUDCliente(CRUDBase[Cliente, ClienteCreate, ClienteUpdate]):
    pass

crud_cliente = CRUDCliente(Cliente) 