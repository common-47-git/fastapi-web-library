import uuid

from sqlalchemy import select

from backend.src.authors.models import AuthorsModel
from backend.src.books.models import BooksModel
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.books_tags.models import BooksTagsModel
from backend.src.database import session_local
from backend.src.repository import SQLAlchemyRepository
from backend.src.tags.models import TagsModel
from backend.src.users.models import UsersModel
from backend.src.users_books.models import UsersBooksModel


class BooksRepository(SQLAlchemyRepository):
    alchemy_model: type[BooksModel] = BooksModel

    async def read_books_by_user_id(
        self,
        user_id: uuid.UUID,
    ):
        async with session_local() as session:
            stmt = (
                select(
                    self.alchemy_model,
                    UsersBooksModel.book_shelf,
                    UsersBooksModel.user_id,
                )
                .join(UsersBooksModel)
                .join(UsersModel)
                .where(UsersModel.user_id == user_id)
            )
            result = await session.execute(stmt)
            rows = result.all()
            return [
                {
                    **book.__dict__,
                    "book_shelf": book_shelf,
                    "user_id": user_id,
                }
                for book, book_shelf, user_id in rows
            ]

    async def read_books_by_author_id(
        self,
        author_id: uuid.UUID,
    ) -> list[BooksModel]:
        async with session_local() as session:
            stmt = (
                select(self.alchemy_model)
                .join(BooksAuthorsModel)
                .join(AuthorsModel)
                .where(AuthorsModel.author_id == author_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def read_books_by_tag_id(
        self,
        tag_id: uuid.UUID,
    ) -> list[BooksModel]:
        async with session_local() as session:
            stmt = (
                select(self.alchemy_model)
                .join(BooksTagsModel)
                .join(TagsModel)
                .where(TagsModel.tag_id == tag_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
