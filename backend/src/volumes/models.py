import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database import Base


class VolumesModel(Base):
    __tablename__ = "volumes"

    volume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.book_id"), nullable=False,
    )
    volume_number: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True,
    )
    volume_name: Mapped[str] = mapped_column(String(50), nullable=False)

    volume_book: Mapped["BooksModel"] = relationship(  # noqa: F821
        back_populates="book_volumes",
    )

    volume_chapters: Mapped[list["ChaptersModel"]] = relationship(  # noqa: F821
        back_populates="chapter_volume", cascade="all, delete-orphan",
    )
