from sqlalchemy import and_, select

from backend.src.books_authors import schemas as books_authors_schemas
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.database import async_session_dependency


async def read_books_authors_by_id(
    session: async_session_dependency,
    books_authors: books_authors_schemas.BooksAuthorsBase,
):
    stmt = select(BooksAuthorsModel).where(
        and_(
            BooksAuthorsModel.book_id == books_authors.book_id,
            BooksAuthorsModel.author_id == books_authors.author_id,
        ),
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def delete_books_authors_by_id(
    books_authors: books_authors_schemas.BooksAuthorsDelete,
    session: async_session_dependency,
):
    entry_to_delete = await read_books_authors_by_id(
        session=session, books_authors=books_authors,
    )
    if not entry_to_delete:
        return None
    await session.delete(entry_to_delete)
    await session.commit()
    return entry_to_delete
