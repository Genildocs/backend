from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vidracaria_user:iS2YdVOM5e3tqEB05ELfuJuhe7g4Zkih@dpg-cvveejjuibrs73bcua40-a.oregon-postgres.render.com/vidracaria_2v72")

# Engine do SQLAlchemy
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    poolclass=NullPool
)

# Sessão assíncrona
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para os modelos
Base = declarative_base()

# Função para obter a sessão do banco
async def get_db() -> Generator:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 