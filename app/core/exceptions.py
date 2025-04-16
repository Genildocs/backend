from fastapi import HTTPException, status

class CustomHTTPException(HTTPException):
    """Exceção base personalizada."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class ValidationError(CustomHTTPException):
    """Erro de validação."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class NotFoundError(CustomHTTPException):
    """Recurso não encontrado."""
    def __init__(self, resource: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} não encontrado"
        )

class UnauthorizedError(CustomHTTPException):
    """Não autorizado."""
    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class ForbiddenError(CustomHTTPException):
    """Acesso negado."""
    def __init__(self, detail: str = "Acesso negado"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class ConflictError(CustomHTTPException):
    """Conflito (recurso já existe)."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        ) 