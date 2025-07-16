import uuid

from sqlalchemy import and_, select

from backend.src.database import session_local
from backend.src.enums import BookShelfEnum
from backend.src.repository import SQLAlchemyRepository
from backend.src.users_books.models import UsersBooksModel


class UsersBooksRepository(SQLAlchemyRepository):
    alchemy_model: type[UsersBooksModel] = UsersBooksModel

    async def read_user_book_by_ids(
        self,
        user_id: uuid.UUID,
        book_id: uuid.UUID,
    ) -> UsersBooksModel | None:
        async with session_local() as session:
            stmt = select(self.alchemy_model).where(
                and_(
                    self.alchemy_model.book_id == book_id,
                    self.alchemy_model.user_id == user_id,
                ),
            )
            result = await session.execute(stmt)
            return result.scalars().first()

    async def update_shelf_by_ids(
        self,
        user_id: uuid.UUID,
        book_id: uuid.UUID,
        book_shelf: str,
    ) -> UsersBooksModel | None:
        async with session_local() as session:
            stmt = select(self.alchemy_model).where(
                and_(
                    self.alchemy_model.book_id == book_id,
                    self.alchemy_model.user_id == user_id,
                ),
            )
            result = await session.execute(stmt)
            user_book = result.scalars().first()

            if not user_book:
                return None
            user_book.book_shelf = BookShelfEnum(book_shelf)
            await session.commit()
            await session.refresh(user_book)
            return user_book

    async def delete_users_books_by_ids(
        self,
        user_id: uuid.UUID,
        book_id: uuid.UUID,
    ) -> UsersBooksModel | None:
        async with session_local() as session:
            entry_to_delete = await self.read_user_book_by_ids(
                user_id=user_id,
                book_id=book_id,
            )
            if not entry_to_delete:
                return None

            await session.delete(entry_to_delete)
            await session.commit()
            return entry_to_delete
