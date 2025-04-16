from fastapi import APIRouter

from app.api.v1.endpoints import auth, clientes, vendedores, vendas, notifications, password_reset

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
api_router.include_router(vendedores.router, prefix="/vendedores", tags=["vendedores"])
api_router.include_router(vendas.router, prefix="/vendas", tags=["vendas"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(password_reset.router, prefix="/password-reset", tags=["password-reset"]) 