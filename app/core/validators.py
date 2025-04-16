import re
from typing import Optional

def validate_cpf(cpf: str) -> bool:
    """Valida um CPF."""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Validação do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = 11 - (soma % 11)
    if resto > 9:
        resto = 0
    if resto != int(cpf[9]):
        return False
    
    # Validação do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = 11 - (soma % 11)
    if resto > 9:
        resto = 0
    if resto != int(cpf[10]):
        return False
    
    return True

def validate_phone(phone: str) -> bool:
    """Valida um número de telefone brasileiro."""
    # Remove caracteres não numéricos
    phone = re.sub(r'[^0-9]', '', phone)
    
    # Verifica se tem entre 10 e 11 dígitos
    if len(phone) not in [10, 11]:
        return False
    
    # Verifica se começa com dígito válido
    if not phone[0] in ['2', '3', '4', '5', '6', '7', '8', '9']:
        return False
    
    return True

def validate_email(email: str) -> bool:
    """Valida um endereço de e-mail."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_input(text: str) -> str:
    """Remove caracteres potencialmente perigosos de uma string."""
    # Remove tags HTML
    text = re.sub(r'<[^>]+>', '', text)
    # Remove caracteres especiais, mantendo apenas letras, números e alguns caracteres comuns
    text = re.sub(r'[^\w\s.,-]', '', text)
    return text.strip() 