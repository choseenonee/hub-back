from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models, hash, CRUD


class ValidationByEmail(BaseModel):
    email: str
    password: str


class ValidationByNick(BaseModel):
    nickname: str
    password: str


class ValidationByPhoneNumber(BaseModel):
    phone_number: str
    password: str


def authorization_by_email(db: Session, email: str, password: str):
    user = CRUD.get_user_by_email(db, email)
    return hash.check_hash_password(password, user.hashed_password)


def authorization_by_phone_number(db: Session, phone_number: str, password: str):
    user = CRUD.get_user_by_phone_number(db, phone_number)
    return hash.check_hash_password(password, user.hashed_password)