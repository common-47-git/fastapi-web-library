from collections.abc import Sequence

from sqlalchemy import select

from backend.src.books.models import BooksModel
from backend.src.database import async_session_dependency
from backend.src.users.models import UsersModel
from backend.src.users_books.models import UsersBooksModel


async def get_user_books(
    session: async_session_dependency,
    username: str,
) -> Sequence[BooksModel] | None:
    query = (
        select(BooksModel)
        .join(UsersBooksModel)
        .join(UsersModel)
        .filter(UsersModel.username == username)
    )
    result = await session.execute(query)
    return result.scalars().all()
