from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    telefone = Column(String(15), nullable=False)
    endereco = Column(String(100), nullable=False)
    numero = Column(String(10), nullable=False)
    bairro = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    cep = Column(String(9), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now()) 