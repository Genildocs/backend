from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(15), nullable=False)
    senha = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamento com permissões
    permissions = relationship("Permission", secondary="administrador_permissions", back_populates="administradores")

    def has_permission(self, permission_name: str) -> bool:
        """Verifica se o administrador tem uma permissão específica"""
        return any(p.name == permission_name for p in self.permissions)

    def has_module_permission(self, module: str, action: str) -> bool:
        """Verifica se o administrador tem permissão em um módulo específico"""
        permission_name = f"{action}_{module}"
        return self.has_permission(permission_name) 