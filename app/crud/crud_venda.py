from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.venda import Venda
from app.schemas.venda import VendaCreate, VendaUpdate

class CRUDVenda(CRUDBase[Venda, VendaCreate, VendaUpdate]):
    pass

crud_venda = CRUDVenda(Venda) 