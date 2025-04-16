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
    Envia um e-mail usando SMTP.
    
    Args:
        to_email: E-mail do destinatário
        subject: Assunto do e-mail
        body: Corpo do e-mail em HTML
    
    Returns:
        bool: True se o e-mail foi enviado com sucesso, False caso contrário
    """
    try:
        # Cria a mensagem
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        
        # Adiciona o corpo do e-mail
        msg.attach(MIMEText(body, "html"))
        
        # Conecta ao servidor SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            
        logger.info(f"E-mail enviado com sucesso para {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {to_email}: {str(e)}")
        return False

def send_password_reset_email(to_email: str, reset_token: str) -> bool:
    """
    Envia um e-mail com o link para redefinição de senha.
    
    Args:
        to_email: E-mail do usuário
        reset_token: Token para redefinição de senha
    
    Returns:
        bool: True se o e-mail foi enviado com sucesso, False caso contrário
    """
    # URL do frontend para redefinição de senha
    reset_url = f"https://seu-frontend.com/reset-password?token={reset_token}"
    
    # Corpo do e-mail em HTML
    body = f"""
    <html>
        <body>
            <h2>Redefinição de Senha</h2>
            <p>Olá,</p>
            <p>Recebemos uma solicitação para redefinir sua senha.</p>
            <p>Clique no link abaixo para criar uma nova senha:</p>
            <p><a href="{reset_url}">{reset_url}</a></p>
            <p>Se você não solicitou esta redefinição, ignore este e-mail.</p>
            <p>Este link expira em 1 hora.</p>
            <p>Atenciosamente,<br>Equipe Vidraçaria dos Anjos</p>
        </body>
    </html>
    """
    
    return send_email(to_email, "Redefinição de Senha - Vidraçaria dos Anjos", body) 