from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.database import BaseAlchemyModel


class BooksAuthorsModel(BaseAlchemyModel):
    __tablename__ = "books_authors"

    book_id: Mapped[UUID] = mapped_column(
        ForeignKey("books.book_id"),
        primary_key=True,
    )
    author_id: Mapped[UUID] = mapped_column(
        ForeignKey("authors.author_id"),
        primary_key=True,
    )
