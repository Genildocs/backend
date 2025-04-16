import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings

def init_database():
    # Conectar ao PostgreSQL
    conn = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Criar cursor
    cur = conn.cursor()
    
    try:
        # Criar usuário se não existir
        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT FROM pg_catalog.pg_user
                    WHERE usename = 'vidracaria_user'
                ) THEN
                    CREATE USER vidracaria_user WITH PASSWORD 'password';
                END IF;
            END
            $$;
        """)
        
        # Criar banco de dados se não existir
        cur.execute("""
            SELECT 'CREATE DATABASE vidracaria'
            WHERE NOT EXISTS (
                SELECT FROM pg_database WHERE datname = 'vidracaria'
            );
        """)
        
        print("Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
    
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_database() 