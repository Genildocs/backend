from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.vendedor import Vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate

class CRUDVendedor(CRUDBase[Vendedor, VendedorCreate, VendedorUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Vendedor]:
        return db.query(Vendedor).filter(Vendedor.email == email).first()

crud_vendedor = CRUDVendedor(Vendedor) 