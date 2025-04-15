from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    cpf: str = Field(..., min_length=11, max_length=14)
    telefone: str = Field(..., max_length=15)
    endereco: str = Field(..., max_length=100)
    numero: str = Field(..., max_length=10)
    bairro: str = Field(..., max_length=50)
    cidade: str = Field(..., max_length=50)
    cep: str = Field(..., max_length=9)


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    telefone: Optional[str] = Field(None, max_length=15)
    endereco: Optional[str] = Field(None, max_length=100)
    numero: Optional[str] = Field(None, max_length=10)
    bairro: Optional[str] = Field(None, max_length=50)
    cidade: Optional[str] = Field(None, max_length=50)
    cep: Optional[str] = Field(None, max_length=9)


class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime


class ClienteList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    nome: str
    cpf: str
    telefone: str 