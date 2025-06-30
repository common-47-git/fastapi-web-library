import uuid

from backend.src import http_exceptions
from backend.src.books.models import BooksModel
from backend.src.books.services import BooksServices


class BooksDeps:
    @staticmethod
    async def one_exists(book_id: uuid.UUID) -> BooksModel:
        book = await BooksServices().read_one_by_property(
            property_name=BooksModel.book_id.key,
            property_value=book_id,
        )
        if book is None:
            raise http_exceptions.NotFound404
        return book
