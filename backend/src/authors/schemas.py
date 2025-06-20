from pydantic import UUID4, BaseModel, Field


class AuthorBase(BaseModel):
    author_name: str = Field(max_length=50)
    author_surname: str = Field(max_length=50)


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    author_id: UUID4


class AuthorDelete(AuthorBase):
    author_id: UUID4


class AuthorInDB(AuthorBase):
    author_id: UUID4
