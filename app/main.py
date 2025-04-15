from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, clientes, vendedores, vendas

app = FastAPI(
    title="API Vidraçaria dos Anjos",
    description="API para gerenciamento de vendas, orçamentos e clientes da Vidraçaria dos Anjos",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas
app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(vendedores.router)
app.include_router(vendas.router)

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API da Vidraçaria dos Anjos",
        "docs": "/docs",
        "redoc": "/redoc"
    } 