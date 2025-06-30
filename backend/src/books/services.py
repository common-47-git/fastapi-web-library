import uuid
from collections.abc import Sequence

from backend.src import http_exceptions
from backend.src.books.models import BooksModel
from backend.src.books.repository import BooksRepository
from backend.src.services import BaseServices


class BooksServices(BaseServices):
    alchemy_model: type[BooksModel] = BooksModel
    repository: type[BooksRepository] = BooksRepository

    async def read_books_by_author_id(
        self,
        author_id: uuid.UUID,
    ) -> Sequence[BooksModel]:
        books = await self.repository().read_books_by_author_id(
            author_id=author_id,
        )
        if not books:
            raise http_exceptions.NotFound404
        return books
