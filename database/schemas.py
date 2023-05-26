from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict


class Authorization(BaseModel):
    email: str | None = None
    nickname: str | None = None
    phone_number: str | None = None
    password: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    nickname: str
    name: str
    surname: str
    grade: int
    contacts: Dict[str, str] = []
    description: str | None = ''
    avatar_uuid: UUID | None = None  # UUID
    is_admin: bool | None = False
    is_teacher: bool | None = False


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: str | None = None
    phone_number: str | None = None
    password: str


class UserUpdate(BaseModel):
    nickname: str | None = None
    name: str | None = None
    surname: str | None = None
    grade: int | None = None
    contacts: Dict[str, str] = []
    description: str | None = ''
    avatar_uuid: UUID | None = None  # UUID
    is_admin: bool | None = False
    is_teacher: bool | None = False


class AuthUpdate(BaseModel):
    email: str | None = None
    nickname: str | None = None
    phone_number: str | None = None
    password: str | None = None


class CreateTag(BaseModel):
    user_id: int
    tag: str


class Tag(CreateTag):
    id: int

    class Config:
        orm_mode = True


class CreateFavColab(BaseModel):
    user_id: int
    colab_id: int


class FavColab(CreateFavColab):
    id: int

    class Config:
        orm_mode = True


class CreateFavArchive(BaseModel):
    user_id: int
    archive_id: int


class FavArchive(CreateFavArchive):
    id: int

    class Config:
        orm_mode = True


class CreateFavUser(BaseModel):
    user_id: int
    fav_user_id: int


class FavUser(CreateFavUser):
    id: int

    class Config:
        orm_mode = True
