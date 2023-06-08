from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from database.CRUD import get_user_auth
from database.hash import check_hash_password
from database import models
from database.database import SessionLocal, engine
from fastapi import HTTPException, status
from jose import jwt, JWTError
from .schemas import Token, TokenData


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600


def get_login(login: str):
    email = None
    nickname = None
    phone_number = None

    if login.isdigit():
        phone_number = login
    elif "@" in login:
        email = login
    else:
        nickname = login
    return email, nickname, phone_number


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_for_access(db: Session, login: str, password: str):
    email, nickname, phone_number = get_login(login)
    auth = get_user_auth(db=db, email=email, nickname=nickname, phone_number=phone_number)

    if not check_hash_password(password, auth.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='wrong password')
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": auth.nickname}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    email, nickname, phone_number = get_login(token_data.username)
    auth = get_user_auth(db=db, email=email, nickname=nickname, phone_number=phone_number)
    if auth is None:
        raise credentials_exception
    return auth.user
