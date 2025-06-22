import uuid
from collections.abc import Sequence

from sqlalchemy import select

from backend.src.authors.models import AuthorsModel
from backend.src.books.models import BooksModel
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.database import async_session_dependency


async def read_books_by_author_id(
    author_id: uuid.UUID,
    session: async_session_dependency,
) -> Sequence[BooksModel] | None:
    stmt = (
        select(BooksModel)
        .join(BooksAuthorsModel)
        .join(AuthorsModel)
        .where(AuthorsModel.author_id == author_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()
