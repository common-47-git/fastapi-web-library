import uuid

from pydantic import BaseModel


class UsersBooksBase(BaseModel):
    user_id: uuid.UUID
    book_id: uuid.UUID


class UsersBooksFind(UsersBooksBase):
    pass


class UsersBooksCreate(UsersBooksBase):
    book_shelf: str | None = None


class UsersBooksRead(UsersBooksBase):
    book_shelf: str | None = None


class UsersBooksUpdate(UsersBooksBase):
    book_shelf: str


class UsersBooksDelete(UsersBooksBase):
    pass


class UsersBooksInDB(UsersBooksBase):
    book_shelf: str | None = None
