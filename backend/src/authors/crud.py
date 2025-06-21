import uuid

from sqlalchemy import select

from backend.src.authors.models import AuthorsModel
from backend.src.books.models import BooksModel
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.database import async_session_dependency


async def read_authors_by_book_id(
    book_id: uuid.UUID, session: async_session_dependency,
):
    stmt = (
        select(AuthorsModel)
        .join(BooksAuthorsModel)
        .join(BooksModel)
        .where(BooksModel.book_id == book_id)
    )
    result = await session.execute(stmt)
    authors = result.scalars().all()

    return authors
