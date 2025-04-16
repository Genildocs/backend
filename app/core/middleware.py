from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

def setup_middleware(app: FastAPI):
    # Configuração do CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "https://sales-pro-ashen.vercel.app",
            "http://127.0.0.1:8000",
            "http://127.0.0.1:5173",
            "http://localhost:8000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware para compressão GZip
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Middleware para headers de segurança
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https://cdn.jsdelivr.net"
        return response

    # Middleware para rate limiting
    @app.middleware("http")
    async def rate_limit(request, call_next):
        # TODO: Implementar rate limiting
        # Por enquanto, apenas passa a requisição
        response = await call_next(request)
        return response 