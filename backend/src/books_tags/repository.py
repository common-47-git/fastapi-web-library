import uuid

from sqlalchemy import and_, select

from backend.src.books_tags.models import BooksTagsModel
from backend.src.database import session_local
from backend.src.repository import SQLAlchemyRepository


class BooksTagsRepository(SQLAlchemyRepository):
    alchemy_model: type[BooksTagsModel] = BooksTagsModel

    async def read_books_tags_by_id(
        self,
        book_id: uuid.UUID,
        tag_id: uuid.UUID,
    ) -> BooksTagsModel | None:
        async with session_local() as session:
            stmt = select(self.alchemy_model).where(
                and_(
                    self.alchemy_model.book_id == book_id,
                    self.alchemy_model.tag_id == tag_id,
                ),
            )
            result = await session.execute(stmt)
            return result.scalars().first()

    async def delete_books_tags_by_id(
        self,
        book_id: uuid.UUID,
        tag_id: uuid.UUID,
    ) -> BooksTagsModel | None:
        async with session_local() as session:
            entry_to_delete = await self.read_books_tags_by_id(
                book_id=book_id,
                tag_id=tag_id,
            )
            if not entry_to_delete:
                return None

            await session.delete(entry_to_delete)
            await session.commit()
            return entry_to_delete
