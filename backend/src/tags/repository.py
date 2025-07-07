import uuid
from collections.abc import Sequence

from sqlalchemy import select

from backend.src.books.models import BooksModel
from backend.src.books_tags.models import BooksTagsModel
from backend.src.database import session_local
from backend.src.repository import SQLAlchemyRepository
from backend.src.tags.models import TagsModel


class TagsRepository(SQLAlchemyRepository):
    alchemy_model: type[TagsModel] = TagsModel

    async def read_tags_by_book_id(
        self,
        book_id: uuid.UUID,
    ) -> list[TagsModel]:
        async with session_local() as session:
            stmt = (
                select(TagsModel)
                .join(BooksTagsModel)
                .join(BooksModel)
                .where(BooksModel.book_id == book_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
