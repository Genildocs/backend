from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from datetime import datetime, timedelta

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vendedor_id = Column(String(36), ForeignKey("vendedores.id"), nullable=False)
    token = Column(String(100), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    used_at = Column(DateTime, nullable=True)

    def is_valid(self) -> bool:
        """Verifica se o token ainda é válido."""
        return (
            self.used_at is None and
            datetime.utcnow() < self.expires_at
        )

    @classmethod
    def create_token(cls, vendedor_id: str) -> "PasswordResetToken":
        """Cria um novo token de redefinição de senha."""
        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        return cls(
            vendedor_id=vendedor_id,
            token=token,
            expires_at=expires_at
        ) 