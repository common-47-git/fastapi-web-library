import uuid
from backend.src.books.repository import BooksRepository
from backend.src.books.models import BooksModel
from backend.src import http_exceptions


async def book_exists_dep(book_id: uuid.UUID) -> BooksModel:
    book = await BooksRepository().read_one_by_property(
        property_name=BooksModel.book_id.key,
        property_value=book_id,
    )
    if book is None:
        raise http_exceptions.NotFound404
    return book
