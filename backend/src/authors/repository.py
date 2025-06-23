import uuid
from collections.abc import Sequence

from sqlalchemy import select

from backend.src.authors.models import AuthorsModel
from backend.src.books.models import BooksModel
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.database import session_local
from backend.src.repository import SQLAlchemyRepository


class AuthorsRepository(SQLAlchemyRepository):
    alchemy_model: type[AuthorsModel] = AuthorsModel

    async def read_authors_by_book_id(
        self,
        book_id: uuid.UUID,
    ) -> Sequence[AuthorsModel] | None:
        async with session_local() as session:
            stmt = (
                select(self.alchemy_model)
                .join(BooksAuthorsModel)
                .join(BooksModel)
                .where(BooksModel.book_id == book_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
