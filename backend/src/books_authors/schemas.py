from pydantic import UUID4, BaseModel


class BooksAuthorsBase(BaseModel):
    book_id: UUID4
    author_id: UUID4


class BooksAuthorsCreate(BooksAuthorsBase):
    pass


class BooksAuthorsRead(BooksAuthorsBase):
    pass


class BooksAuthorsUpate(BooksAuthorsBase):
    pass


class BooksAuthorsDelete(BooksAuthorsBase):
    pass


class BooksAuthorsInDB(BooksAuthorsBase):
    pass
