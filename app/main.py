from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import setup_middleware
from app.routes import auth, clientes, vendedores, vendas, password_reset, notifications
from app.core.database import engine, Base
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criação da aplicação
app = FastAPI(
    title="API Vidraçaria dos Anjos",
    description="API para gerenciamento de vendas e orçamentos",
    version="1.0.0"
)

# Configuração dos middlewares
setup_middleware(app)

# Criação das tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Inclusão das rotas
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(vendedores.router, prefix="/vendedores", tags=["Vendedores"])
app.include_router(vendas.router, prefix="/vendas", tags=["Vendas"])
app.include_router(password_reset.router, prefix="/password-reset", tags=["Recuperação de Senha"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notificações"])

@app.get("/health")
async def health_check():
    """Endpoint para verificar a saúde da aplicação."""
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API da Vidraçaria dos Anjos",
        "docs": "/docs",
        "redoc": "/redoc"
    } 