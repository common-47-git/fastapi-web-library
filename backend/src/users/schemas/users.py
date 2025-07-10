import uuid
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    user_id: uuid.UUID
    registration_date: date | None = None
    disabled: bool | None = None


class UserUpdate(BaseModel):
    pass


class UserInDB(UserBase):
    user_id: uuid.UUID
    disabled: bool | None = None
    registration_date: date
    password: str
