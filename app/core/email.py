from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dotenv import load_dotenv
import logging

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração de logging
logger = logging.getLogger(__name__)

# Configurações do servidor SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@vidracaria.com")

def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Função temporariamente desabilitada - apenas loga a tentativa de envio
    """
    logger.info(f"Tentativa de envio de email para {to_email}")
    logger.info(f"Assunto: {subject}")
    logger.info("Serviço de email temporariamente desabilitado")
    return True

def send_password_reset_email(to_email: str, reset_token: str) -> bool:
    """
    Função temporariamente desabilitada - apenas loga a tentativa de envio
    """
    logger.info(f"Tentativa de envio de email de recuperação de senha para {to_email}")
    logger.info(f"Token de reset: {reset_token}")
    logger.info("Serviço de email temporariamente desabilitado")
    return True 