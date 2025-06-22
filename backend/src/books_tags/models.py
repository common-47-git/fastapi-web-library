from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.database import BaseAlchemyModel


class BooksTagsModel(BaseAlchemyModel):
    __tablename__ = "books_tags"

    book_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("books.book_id"),
        primary_key=True,
        nullable=False,
    )

    tag_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tags.tag_id"),
        primary_key=True,
        nullable=False,
    )
