import datetime
import uuid

from sqlalchemy import DATE, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database import BaseAlchemyModel
from backend.src.users_books.models import (
    UsersBooksModel,  # noqa: F401 for back_populates
)


class UsersModel(BaseAlchemyModel):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    registration_date: Mapped[datetime.date] = mapped_column(
        DATE,
        default=datetime.datetime.now(tz=datetime.UTC).date(),
        nullable=True,
    )

    user_books: Mapped[list["BooksModel"]] = relationship(
        back_populates="book_users",
        secondary="users_books",
    )
