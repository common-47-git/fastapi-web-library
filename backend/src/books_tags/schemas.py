from pydantic import UUID4, BaseModel


class BooksTagsBase(BaseModel):
    book_id: UUID4
    tag_id: UUID4


class BooksTagsCreate(BooksTagsBase):
    pass


class BooksTagsRead(BooksTagsBase):
    pass


class BooksTagsUpate(BooksTagsBase):
    pass


class BooksTagsDelete(BooksTagsBase):
    pass


class BooksTagsInDB(BooksTagsBase):
    pass
