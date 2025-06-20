from sqlalchemy import select

from src.books.models import BooksModel
from src.chapters import schemas as chapters_schemas
from src.chapters.models import ChaptersModel
from src.database import async_session_dependency
from src.volumes.models import VolumesModel


async def read_book_chapter(
    book_name: str,
    volume_number: int,
    chapter_number: int,
    session: async_session_dependency,
) -> chapters_schemas.ChapterRead:
    query = (
        select(ChaptersModel)
        .join(VolumesModel, VolumesModel.volume_id == ChaptersModel.volume_id)
        .join(BooksModel, BooksModel.book_id == VolumesModel.book_id)
        .where(ChaptersModel.chapter_number == chapter_number)
        .where(VolumesModel.volume_number == volume_number)
        .where(BooksModel.book_name == book_name)
    )

    result = await session.execute(query)
    chapter = result.scalars().first()
    return chapter
