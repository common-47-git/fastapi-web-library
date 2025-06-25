import uuid

from sqlalchemy import TEXT, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.database import BaseAlchemyModel


class ChaptersModel(BaseAlchemyModel):
    __tablename__ = "chapters"

    chapter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    volume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("volumes.volume_id"),
        nullable=False,
    )
    chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    chapter_name: Mapped[str] = mapped_column(String(50), nullable=False)
    chapter_content: Mapped[str] = mapped_column(TEXT, nullable=False)

    chapter_volume: Mapped["VolumesModel"] = relationship(  # noqa: F821
        back_populates="volume_chapters",
    )

    __table_args__ = (
        UniqueConstraint(
            "chapter_number",
            "volume_id",
            name="uq_chapter_number_volume_id",
        ),
    )
