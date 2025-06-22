import uuid
from datetime import date

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    user_id: uuid.UUID
    registration_date: date | None = None
    disabled: bool | None = None


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    user_id: uuid.UUID
    disabled: bool | None = None
    registration_date: date
    password: str
