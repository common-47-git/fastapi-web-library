from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BooksTagsModel(Base):
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


# BooksTagsModel = Table(
#    "books_tags",
#    Base.metadata,
#    Column(
#        "book_id",
#        UUID(as_uuid=True),
#        ForeignKey("books.book_id"),
#        primary_key=True,
#        nullable=False,
#    ),
#    Column(
#        "tag_id",
#        UUID(as_uuid=True),
#        ForeignKey("tags.tag_id"),
#        primary_key=True,
#        nullable=False,
#    ),
# )
