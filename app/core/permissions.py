from functools import wraps
from fastapi import HTTPException, status
from app.core.security import get_current_user
from app.core.exceptions import ForbiddenError
from app.models.vendedor import Vendedor
from sqlalchemy.orm import Session
from app.core.database import get_db

def require_permission(permission_name: str):
    """
    Decorator para verificar se o usuário tem uma permissão específica.
    
    Args:
        permission_name: Nome da permissão requerida
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtém o e-mail do usuário atual
            email = await get_current_user()
            
            # Obtém a sessão do banco de dados
            db: Session = next(get_db())
            
            # Busca o vendedor
            vendedor = db.query(Vendedor).filter(Vendedor.email == email).first()
            if not vendedor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vendedor não encontrado"
                )
            
            # Verifica a permissão
            if not vendedor.has_permission(permission_name):
                raise ForbiddenError(
                    f"Você não tem permissão para {permission_name}"
                )
            
            # Se tiver permissão, executa a função
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def require_module_permission(module: str, action: str):
    """
    Decorator para verificar se o usuário tem permissão em um módulo específico.
    
    Args:
        module: Nome do módulo (ex: 'vendas', 'clientes')
        action: Ação requerida (ex: 'view', 'create', 'edit', 'delete')
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtém o e-mail do usuário atual
            email = await get_current_user()
            
            # Obtém a sessão do banco de dados
            db: Session = next(get_db())
            
            # Busca o vendedor
            vendedor = db.query(Vendedor).filter(Vendedor.email == email).first()
            if not vendedor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vendedor não encontrado"
                )
            
            # Verifica a permissão
            if not vendedor.has_module_permission(module, action):
                raise ForbiddenError(
                    f"Você não tem permissão para {action} em {module}"
                )
            
            # Se tiver permissão, executa a função
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator 