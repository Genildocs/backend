from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_documento = Column(String(20), unique=True, nullable=False)
    tipo = Column(String(10), nullable=False)  # BUDGET ou ORDER
    status = Column(String(20), nullable=False, default="PENDING")
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    vendedor_id = Column(UUID(as_uuid=True), ForeignKey("vendedores.id"), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    cliente = relationship("Cliente", backref="vendas")
    vendedor = relationship("Vendedor", backref="vendas")
    itens = relationship("Item", backref="venda", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "itens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    venda_id = Column(UUID(as_uuid=True), ForeignKey("vendas.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    material = Column(String(100), nullable=False)
    medidas = Column(String(50), nullable=False)
    cor = Column(String(50), nullable=False)
    espessura = Column(String(50), nullable=False)
    unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now()) 