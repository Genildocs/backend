from fastapi import FastAPI, Depends, HTTPException
from app.core.middleware import setup_middleware
from app.core.database import engine, Base, get_db
from app.api.v1.api import api_router
import logging
from sqlalchemy import text
from datetime import datetime
import psutil
from sqlalchemy.exc import SQLAlchemyError

# Importar todos os modelos para garantir que são criados
from app.models.vendedor import Vendedor
from app.models.cliente import Cliente
from app.models.venda import Venda
from app.models.notification import Notification

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar tabelas do banco de dados com tratamento de erro
try:
    logger.info("Tentando criar tabelas do banco de dados...")
    # Criar tabelas na ordem correta
    Vendedor.__table__.create(bind=engine, checkfirst=True)
    Cliente.__table__.create(bind=engine, checkfirst=True)
    Venda.__table__.create(bind=engine, checkfirst=True)
    Notification.__table__.create(bind=engine, checkfirst=True)
    logger.info("Tabelas criadas com sucesso!")
except SQLAlchemyError as e:
    logger.error(f"Erro ao criar tabelas: {str(e)}")
    logger.warning("A aplicação continuará rodando, mas algumas funcionalidades podem não estar disponíveis")

app = FastAPI(title="Vidraçaria API")

# Configurar middleware
try:
    setup_middleware(app)
    logger.info("Middleware configurado com sucesso!")
except Exception as e:
    logger.error(f"Erro ao configurar middleware: {str(e)}")

# Incluir rotas
try:
    app.include_router(api_router, prefix="/api")
    logger.info("Rotas da API incluídas com sucesso!")
except Exception as e:
    logger.error(f"Erro ao incluir rotas da API: {str(e)}")

@app.get("/health")
async def health_check(db = Depends(get_db)):
    """
    Endpoint de verificação de saúde da aplicação.
    Verifica:
    - Conexão com o banco de dados
    - Uso de memória
    - Uso de CPU
    - Tempo de resposta
    """
    health_info = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "checks": {
            "database": {
                "status": "ok",
                "response_time": None
            },
            "memory": {
                "status": "ok",
                "usage_percent": None
            },
            "cpu": {
                "status": "ok",
                "usage_percent": None
            }
        }
    }

    try:
        # Verificar conexão com o banco
        start_time = datetime.utcnow()
        db.execute(text("SELECT 1"))
        end_time = datetime.utcnow()
        health_info["checks"]["database"]["response_time"] = (end_time - start_time).total_seconds()
        logger.info("Conexão com o banco de dados verificada com sucesso")
    except Exception as e:
        health_info["checks"]["database"]["status"] = "error"
        health_info["checks"]["database"]["error"] = str(e)
        health_info["status"] = "error"
        logger.error(f"Erro na conexão com o banco de dados: {str(e)}")

    try:
        # Verificar uso de memória
        memory = psutil.virtual_memory()
        health_info["checks"]["memory"]["usage_percent"] = memory.percent
        if memory.percent > 90:
            health_info["checks"]["memory"]["status"] = "warning"
            logger.warning(f"Uso de memória alto: {memory.percent}%")
    except Exception as e:
        health_info["checks"]["memory"]["status"] = "error"
        health_info["checks"]["memory"]["error"] = str(e)
        health_info["status"] = "error"
        logger.error(f"Erro ao verificar uso de memória: {str(e)}")

    try:
        # Verificar uso de CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        health_info["checks"]["cpu"]["usage_percent"] = cpu_percent
        if cpu_percent > 90:
            health_info["checks"]["cpu"]["status"] = "warning"
            logger.warning(f"Uso de CPU alto: {cpu_percent}%")
    except Exception as e:
        health_info["checks"]["cpu"]["status"] = "error"
        health_info["checks"]["cpu"]["error"] = str(e)
        health_info["status"] = "error"
        logger.error(f"Erro ao verificar uso de CPU: {str(e)}")

    # Se qualquer check falhou, retornar 503
    if health_info["status"] == "error":
        logger.error("Health check falhou: %s", health_info)
        raise HTTPException(
            status_code=503,
            detail=health_info
        )

    logger.info("Health check concluído com sucesso")
    return health_info 