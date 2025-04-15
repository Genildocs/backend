import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vidracaria_user:iS2YdVOM5e3tqEB05ELfuJuhe7g4Zkih@dpg-cvveejjuibrs73bcua40-a.oregon-postgres.render.com/vidracaria_2v72?sslmode=require")

async def test_connection():
    try:
        # Tenta criar uma conexão com SSL
        conn = await asyncpg.connect(
            DATABASE_URL,
            ssl="require"
        )
        
        # Executa uma query simples
        result = await conn.fetchval('SELECT 1')
        
        print("✅ Conexão com o banco de dados estabelecida com sucesso!")
        print(f"Resultado do teste: {result}")
        
        # Fecha a conexão
        await conn.close()
        
    except Exception as e:
        print("❌ Erro ao conectar com o banco de dados:")
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connection()) 