import uuid
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as POSTGRESQL_ENUM
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.enums import BookShelfEnum

# class UsersBooksModel(Base):
#    __tablename__ = "users_books"
#
#    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.book_id"), primary_key=True, nullable=False)
#    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
#    book_shelf: Mapped[str] = mapped_column(String(30), nullable=True)


class UsersBooksModel(Base):
    __tablename__ = "users_books"

    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("books.book_id"),
        primary_key=True,
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
        nullable=False,
    )

    book_shelf: Mapped[Enum] = mapped_column(
        POSTGRESQL_ENUM(
            BookShelfEnum,
            name="book_shelf_enum",
            values_callable=lambda obj: [e.value for e in obj],
            create_type=False,
        ),
        nullable=True,
        default=None,
    )
