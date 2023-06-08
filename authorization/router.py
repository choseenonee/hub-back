from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.CRUD import get_user_auth
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from database.hash import check_hash_password
from database import models
from database.database import SessionLocal, engine
from database.schemas import User
from jose import jwt, JWTError
import authorization.auth as auth
from .schemas import Token, TokenData


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600


models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


router = APIRouter(
    prefix='/auth',
    tags=['Authorization'],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    token = auth.login_for_access(db=db, login=form_data.username, password=form_data.password)
    return token


@router.get("/me", response_model=User)
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    current_user = auth.get_current_user(token=token, db=db)
    return current_user
