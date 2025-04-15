from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


class VendedorBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    telefone: str = Field(..., max_length=15)


class VendedorCreate(VendedorBase):
    senha: str = Field(..., min_length=6)


class VendedorUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=15)
    senha: Optional[str] = Field(None, min_length=6)
    ativo: Optional[bool] = None


class VendedorResponse(VendedorBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    ativo: bool
    created_at: datetime
    updated_at: datetime


class VendedorList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    nome: str
    email: EmailStr
    telefone: str
    ativo: bool


class VendedorAuth(BaseModel):
    email: EmailStr
    senha: str 