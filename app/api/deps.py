from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.vendedor import Vendedor
from app.crud import crud_vendedor

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_vendedor(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Vendedor:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        vendedor_id: str = payload.get("sub")
        if vendedor_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    vendedor = crud_vendedor.get(db, id=vendedor_id)
    if vendedor is None:
        raise credentials_exception
    return vendedor 