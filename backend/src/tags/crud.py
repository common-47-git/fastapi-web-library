from uuid import UUID

from sqlalchemy import select

from src.books.models import BooksModel
from src.books_tags.models import BooksTagsModel
from src.database import async_session_dependency
from src.tags import schemas as tags_schemas
from src.tags.models import TagsModel


async def read_tags_by_book_id(
    book_id: UUID, session: async_session_dependency,
) -> list[tags_schemas.TagRead]:
    stmt = (
        select(TagsModel)
        .join(BooksTagsModel)
        .join(BooksModel)
        .where(BooksModel.book_id == book_id)
    )
    result = await session.execute(stmt)
    tags = result.scalars().all()

    return tags
