import uuid
from enum import Enum

from sqlalchemy import DATE, String
from sqlalchemy.dialects.postgresql import ENUM as POSTGRESQL_ENUM
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database import BaseAlchemyModel
from backend.src.enums import TranslationStatusEnum


class BooksModel(BaseAlchemyModel):
    __tablename__ = "books"
    # [python] - [sqlalch] types
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    book_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    book_country: Mapped[str] = mapped_column(String(50), nullable=True)
    book_release_date: Mapped[DATE] = mapped_column(DATE, nullable=True)
    book_translation_status: Mapped[Enum] = mapped_column(
        POSTGRESQL_ENUM(
            TranslationStatusEnum,
            name="translation_status_enum",
            values_callable=lambda obj: [e.value for e in obj],
            create_type=False,
        ),
        nullable=True,
        default=TranslationStatusEnum.ABSENT,
    )
    book_description: Mapped[str] = mapped_column(String(1500), nullable=True)
    book_cover: Mapped[str] = mapped_column(String(500), nullable=False)

    book_authors: Mapped[list["AuthorsModel"]] = relationship(  # noqa: F821
        back_populates="author_books",
        secondary="books_authors",
    )

    book_volumes: Mapped[list["VolumesModel"]] = relationship(  # noqa: F821
        back_populates="volume_book",
        cascade="all, delete-orphan",
    )

    book_tags: Mapped[list["TagsModel"]] = relationship(  # noqa: F821
        back_populates="tag_books",
        secondary="books_tags",
    )
