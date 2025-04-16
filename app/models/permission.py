from sqlalchemy import Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

# Tabela de associação entre vendedores e permissões
vendedor_permissions = Table(
    'vendedor_permissions',
    Base.metadata,
    Column('vendedor_id', String(36), ForeignKey('vendedores.id')),
    Column('permission_id', String(36), ForeignKey('permissions.id'))
)

# Tabela de associação entre administradores e permissões
administrador_permissions = Table(
    'administrador_permissions',
    Base.metadata,
    Column('administrador_id', String(36), ForeignKey('administradores.id')),
    Column('permission_id', String(36), ForeignKey('permissions.id'))
)

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    module = Column(String(50), nullable=False)  # Ex: 'vendas', 'clientes', 'financeiro'
    is_active = Column(Boolean, default=True)

    # Relacionamento com vendedores
    vendedores = relationship("Vendedor", secondary=vendedor_permissions, back_populates="permissions")
    
    # Relacionamento com administradores
    administradores = relationship("Administrador", secondary=administrador_permissions, back_populates="permissions")

    @classmethod
    def create_default_permissions(cls):
        """Cria as permissões padrão do sistema."""
        return [
            cls(
                name="view_vendas",
                description="Visualizar vendas",
                module="vendas"
            ),
            cls(
                name="create_vendas",
                description="Criar vendas",
                module="vendas"
            ),
            cls(
                name="edit_vendas",
                description="Editar vendas",
                module="vendas"
            ),
            cls(
                name="delete_vendas",
                description="Excluir vendas",
                module="vendas"
            ),
            cls(
                name="view_clientes",
                description="Visualizar clientes",
                module="clientes"
            ),
            cls(
                name="create_clientes",
                description="Criar clientes",
                module="clientes"
            ),
            cls(
                name="edit_clientes",
                description="Editar clientes",
                module="clientes"
            ),
            cls(
                name="delete_clientes",
                description="Excluir clientes",
                module="clientes"
            ),
            cls(
                name="view_financeiro",
                description="Visualizar financeiro",
                module="financeiro"
            ),
            cls(
                name="edit_financeiro",
                description="Editar financeiro",
                module="financeiro"
            ),
            cls(
                name="view_relatorios",
                description="Visualizar relatórios",
                module="relatorios"
            ),
            cls(
                name="view_configuracoes",
                description="Visualizar configurações",
                module="configuracoes"
            ),
            cls(
                name="edit_configuracoes",
                description="Editar configurações",
                module="configuracoes"
            ),
            cls(
                name="view_notifications",
                description="Visualizar notificações",
                module="notifications"
            ),
            cls(
                name="create_notifications",
                description="Criar notificações",
                module="notifications"
            ),
            cls(
                name="edit_notifications",
                description="Editar notificações",
                module="notifications"
            ),
            cls(
                name="delete_notifications",
                description="Excluir notificações",
                module="notifications"
            ),
            # Permissões específicas para administradores
            cls(
                name="manage_vendedores",
                description="Gerenciar vendedores",
                module="administracao"
            ),
            cls(
                name="manage_administradores",
                description="Gerenciar administradores",
                module="administracao"
            ),
            cls(
                name="manage_permissions",
                description="Gerenciar permissões",
                module="administracao"
            ),
            cls(
                name="view_audit_logs",
                description="Visualizar logs de auditoria",
                module="administracao"
            )
        ] 