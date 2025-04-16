from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
from dotenv import load_dotenv

# Carrega o arquivo .env apropriado
is_production = os.getenv("RENDER", "false").lower() == "true"
env_file = ".env" if is_production else ".env.local"
load_dotenv(env_file)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=env_file,
        env_file_encoding='utf-8'
    )

    PROJECT_NAME: str = "Vidraçaria dos Anjos"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # JWT
    JWT_SECRET_KEY: str = "sua_chave_secreta_aqui_mude_em_producao"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/dbname"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "seu_email@gmail.com"
    SMTP_PASSWORD: str = "sua_senha_de_app"
    EMAIL_FROM: str = "noreply@vidracaria.com"

settings = Settings() 