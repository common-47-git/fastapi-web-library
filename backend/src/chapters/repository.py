import uuid

from sqlalchemy import select

from backend.src.books.models import BooksModel
from backend.src.chapters.models import ChaptersModel
from backend.src.database import session_local
from backend.src.repository import SQLAlchemyRepository
from backend.src.volumes.models import VolumesModel


class ChaptersRepository(SQLAlchemyRepository):
    alchemy_model: type[ChaptersModel] = ChaptersModel

    async def read_book_chapter_by_book_name(
        self,
        book_name: str,
        volume_number: int,
        chapter_number: int,
    ) -> ChaptersModel | None:
        async with session_local() as session:
            query = (
                select(self.alchemy_model)
                .join(
                    VolumesModel,
                    VolumesModel.volume_id == self.alchemy_model.volume_id,
                )
                .join(
                    BooksModel,
                    BooksModel.book_id == VolumesModel.book_id,
                )
                .where(ChaptersModel.chapter_number == chapter_number)
                .where(VolumesModel.volume_number == volume_number)
                .where(BooksModel.book_name == book_name)
            )

            result = await session.execute(query)
            return result.scalars().first()

    async def read_book_chapter_by_book_id(
        self,
        book_id: uuid.UUID,
        volume_number: int,
        chapter_number: int,
    ) -> ChaptersModel | None:
        async with session_local() as session:
            query = (
                select(self.alchemy_model)
                .join(
                    VolumesModel,
                    VolumesModel.volume_id == self.alchemy_model.volume_id,
                )
                .join(
                    BooksModel,
                    BooksModel.book_id == VolumesModel.book_id,
                )
                .where(ChaptersModel.chapter_number == chapter_number)
                .where(VolumesModel.volume_number == volume_number)
                .where(BooksModel.book_id == book_id)
            )

            result = await session.execute(query)
            return result.scalars().first()
