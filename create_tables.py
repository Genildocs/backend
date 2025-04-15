import asyncio
from app.core.database import engine, Base
from app.models import cliente, vendedor, venda

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    asyncio.run(create_tables()) 