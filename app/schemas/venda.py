from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from .cliente import ClienteList
from .vendedor import VendedorList


class ItemBase(BaseModel):
    quantidade: int = Field(..., gt=0)
    material: str = Field(..., max_length=100)
    medidas: str = Field(..., max_length=50)
    cor: str = Field(..., max_length=50)
    espessura: str = Field(..., max_length=50)
    unitario: Decimal = Field(..., ge=0)
    subtotal: Decimal = Field(..., ge=0)


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    venda_id: UUID
    created_at: datetime


class VendaBase(BaseModel):
    tipo: str = Field(..., pattern="^(BUDGET|ORDER)$")
    cliente_id: UUID
    vendedor_id: UUID
    total: Decimal = Field(..., ge=0)


class VendaCreate(VendaBase):
    itens: List[ItemCreate]


class VendaUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(PENDING|APPROVED|REJECTED|CANCELLED)$")


class VendaResponse(VendaBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    numero_documento: str
    status: str
    cliente: ClienteList
    vendedor: VendedorList
    itens: List[ItemResponse]
    created_at: datetime
    updated_at: datetime


class VendaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    numero_documento: str
    tipo: str
    status: str
    cliente: ClienteList
    total: Decimal
    created_at: datetime 