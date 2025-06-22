from sqlalchemy import and_, select

from backend.src.books_tags import schemas as books_tags_schemas
from backend.src.books_tags.models import BooksTagsModel
from backend.src.database import async_session_dependency


async def read_books_tags_by_id(
    session: async_session_dependency,
    books_tags: books_tags_schemas.BooksTagsBase,
) -> BooksTagsModel | None:
    stmt = select(BooksTagsModel).where(
        and_(
            BooksTagsModel.book_id == books_tags.book_id,
            BooksTagsModel.tag_id == books_tags.tag_id,
        ),
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def delete_books_tags_by_id(
    books_tags: books_tags_schemas.BooksTagsDelete,
    session: async_session_dependency,
) -> BooksTagsModel | None:
    entry_to_delete = await read_books_tags_by_id(
        session=session,
        books_tags=books_tags,
    )
    if not entry_to_delete:
        return None

    await session.delete(entry_to_delete)
    await session.commit()
    return entry_to_delete
