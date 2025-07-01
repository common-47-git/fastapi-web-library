import uuid
from collections.abc import Sequence

from backend.src import http_exceptions
from backend.src.authors.repository import AuthorsRepository
from backend.src.books import schemas as book_schemas
from backend.src.books.models import BooksModel
from backend.src.books.repository import BooksRepository
from backend.src.services import BaseServices
from backend.src.tags.repository import TagsRepository


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

    async def read_full_book_info_by_id(
        self,
        book_id: uuid.UUID,
    ):
        book = await self.repository().read_one_by_property(
            property_name=BooksModel.book_id.key,
            property_value=book_id,
        )
        if book is None:
            raise http_exceptions.NotFound404

        tags = await TagsRepository().read_tags_by_book_id(
            book_id=book_id,
        )
        book_authors = await AuthorsRepository().read_authors_by_book_id(
            book_id=book_id,
        )
        book_shelf = None

        return book_schemas.BookFullInfo(
            **book.__dict__,
            book_tags=tags,
            book_authors=book_authors,
            book_shelf=book_shelf,
        )
