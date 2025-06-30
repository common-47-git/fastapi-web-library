import uuid

from sqlalchemy import and_, select

from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.database import session_local
from backend.src.repository import SQLAlchemyRepository


class BooksAuthorsRepository(SQLAlchemyRepository):
    alchemy_model: type[BooksAuthorsModel] = BooksAuthorsModel

    async def read_books_authors_entry_by_id(
        self,
        book_id: uuid.UUID,
        author_id: uuid.UUID,
    ) -> BooksAuthorsModel | None:
        async with session_local() as session:
            stmt = select(self.alchemy_model).where(
                and_(
                    self.alchemy_model.book_id == book_id,
                    self.alchemy_model.author_id == author_id,
                ),
            )
            result = await session.execute(stmt)
            return result.scalars().first()

    async def delete_books_authors_entry_by_id(
        self,
        book_id: uuid.UUID,
        author_id: uuid.UUID,
    ) -> BooksAuthorsModel | None:
        async with session_local() as session:
            entry_to_delete = await self.read_books_authors_entry_by_id(
                book_id=book_id,
                author_id=author_id,
            )
            if not entry_to_delete:
                return None
            await session.delete(entry_to_delete)
            await session.commit()
            return entry_to_delete
