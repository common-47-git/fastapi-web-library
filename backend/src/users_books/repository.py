import uuid
from collections.abc import Sequence

from sqlalchemy import and_, select

from backend.src.books.models import BooksModel
from backend.src.database import session_local
from backend.src.repository import SQLAlchemyRepository
from backend.src.users.models import UsersModel
from backend.src.users_books.models import UsersBooksModel


class UsersBooksRepository(SQLAlchemyRepository):
    alchemy_model: type[UsersBooksModel] = UsersBooksModel

    async def read_user_books(
        self,
        username: str,
    ) -> list[BooksModel] | None:
        async with session_local() as session:
            query = (
                select(BooksModel)
                .join(UsersBooksModel)
                .join(UsersModel)
                .filter(UsersModel.username == username)
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def read_users_books_by_id(
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

    async def delete_users_books_by_id(
        self,
        user_id: uuid.UUID,
        book_id: uuid.UUID,
    ) -> UsersBooksModel | None:
        async with session_local() as session:
            entry_to_delete = await self.read_users_books_by_id(
                user_id=user_id,
                book_id=book_id,
            )
            if not entry_to_delete:
                return None

            await session.delete(entry_to_delete)
            await session.commit()
            return entry_to_delete
