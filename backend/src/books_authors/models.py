from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.database import Base

# class BooksAuthorsModel(Base):
#    __tablename__ = "books_authors"
#
#    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.book_id"), primary_key=True, nullable=False)
#    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.author_id"), primary_key=True, nullable=False)


# BooksAuthorsModel = Table(
#    "books_authors",
#    Base.metadata,
#    Column(
#        "book_id",
#        UUID(as_uuid=True),
#        ForeignKey("books.book_id"),
#        primary_key=True,
#        nullable=False,
#    ),
#    Column(
#        "author_id",
#        UUID(as_uuid=True),
#        ForeignKey("authors.author_id"),
#        primary_key=True,
#        nullable=False,
#    ),
# )


class BooksAuthorsModel(Base):
    __tablename__ = "books_authors"

    book_id: Mapped[UUID] = mapped_column(
        ForeignKey("books.book_id"),
        primary_key=True,
    )
    author_id: Mapped[UUID] = mapped_column(
        ForeignKey("authors.author_id"),
        primary_key=True,
    )
