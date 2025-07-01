from backend.src import http_exceptions
from backend.src.books_authors import schemas as books_authors_schemas
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.books_authors.repository import BooksAuthorsRepository
from backend.src.services import BaseServices


class BooksAuthorsServices(BaseServices):
    alchemy_model: type[BooksAuthorsModel] = BooksAuthorsModel
    repository: type[BooksAuthorsRepository] = BooksAuthorsRepository

    async def read_books_authors_entry_by_id(
        self,
        books_authors: books_authors_schemas.BooksAuthorsBase,
    ) -> BooksAuthorsModel | None:
        entries = await self.repository().read_books_authors_entry_by_id(
            book_id=books_authors.book_id,
            author_id=books_authors.author_id,
        )
        if entries is None:
            raise http_exceptions.NotFound404
        return entries

    async def delete_books_authors_entry_by_id(
        self,
        book_author: books_authors_schemas.BooksAuthorsDelete,
    ) -> BooksAuthorsModel | None:
        deleted = await self.repository().delete_books_authors_entry_by_id(
            book_id=book_author.book_id,
            author_id=book_author.author_id,
        )
        if deleted is None:
            raise http_exceptions.NotFound404
        return deleted
