from collections.abc import Sequence

from sqlalchemy import select

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
    ) -> Sequence[BooksModel] | None:
        async with session_local() as session:
            query = (
                select(BooksModel)
                .join(UsersBooksModel)
                .join(UsersModel)
                .filter(UsersModel.username == username)
            )
            result = await session.execute(query)
            return result.scalars().all()
