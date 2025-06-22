import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database import BaseAlchemyModel


class TagsModel(BaseAlchemyModel):
    __tablename__ = "tags"

    tag_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    tag_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    tag_books: Mapped[list["BooksModel"]] = relationship(  # noqa: F821
        back_populates="book_tags",
        secondary="books_tags",
    )
