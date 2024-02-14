from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    username: str
    registered_at: datetime
    hashed_password: str
    is_verified: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class SessionUserInput(BaseModel):
    name: str
    last_name: str
    surname: str
    first_corp_number: int
    second_corp_number: int


class SessionCreate(BaseModel):
    session_key: str
    user_id: int
    name: str
    last_name: str
    surname: str
    first_corp_number: int
    second_corp_number: int
    timestamp: datetime


class Session(BaseModel):
    id: int
    session_key: str
    user_id: int
    name: str
    last_name: str
    surname: str
    first_corp_number: int
    second_corp_number: int
    timestamp: datetime


class Photo(BaseModel):
    id: int
    photo_name: str
    user_id: int
    timestamp: datetime


class PhotoCreate(BaseModel):
    photo_name: str
    user_id: int


class CardData(BaseModel):
    session_key: str
    name: str
    last_name: str
    surname: str
    first_corp_number: int
    second_corp_number: int
