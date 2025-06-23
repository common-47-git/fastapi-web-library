import uuid
from collections.abc import Sequence

from sqlalchemy import select

from backend.src.authors.models import AuthorsModel
from backend.src.books.models import BooksModel
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.database import session_local
from backend.src.repository import SQLAlchemyRepository


class BooksRepository(SQLAlchemyRepository):
    alchemy_model: type[BooksModel] = BooksModel

    async def read_books_by_author_id(
        self,
        author_id: uuid.UUID,
    ) -> Sequence[BooksModel] | None:
        async with session_local() as session:
            stmt = (
                select(self.alchemy_model)
                .join(BooksAuthorsModel)
                .join(AuthorsModel)
                .where(AuthorsModel.author_id == author_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
