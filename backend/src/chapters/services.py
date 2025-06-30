from backend.src import http_exceptions
from backend.src.chapters.models import ChaptersModel
from backend.src.chapters.repository import ChaptersRepository
from backend.src.services import BaseServices


class ChaptersServices(BaseServices):
    alchemy_model: type[ChaptersModel] = ChaptersModel
    repository: type[ChaptersRepository] = ChaptersRepository

    async def read_book_chapter(
        self,
        book_name: str,
        volume_number: int,
        chapter_number: int,
    ):
        chapter = await ChaptersRepository().read_book_chapter(
            book_name=book_name,
            volume_number=volume_number,
            chapter_number=chapter_number,
        )
        if chapter is None:
            raise http_exceptions.NotFound404
        return chapter
