import uuid

from pydantic import BaseModel


class UsersBooksBase(BaseModel):
    user_id: uuid.UUID
    book_id: uuid.UUID
    book_shelf: str


class UsersBooksCreate(UsersBooksBase):
    pass


class UsersBooksRead(UsersBooksBase):
    pass


class UsersBooksUpdate(UsersBooksBase):
    pass


class UsersBooksInDB(UsersBooksBase):
    pass

