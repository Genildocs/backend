from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.security import create_access_token
from app.core.database import get_db
from app.crud import crud_vendedor
from app.schemas.vendedor import VendedorCreate, VendedorResponse
from app.core.config import settings

router = APIRouter()

@router.post("/login")
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    vendedor = crud_vendedor.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(vendedor.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
async def register(
    vendedor_in: VendedorCreate,
    db: Session = Depends(get_db)
):
    vendedor = crud_vendedor.get_by_email(db, email=vendedor_in.email)
    if vendedor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    vendedor = crud_vendedor.create(db, obj_in=vendedor_in)
    return vendedor 