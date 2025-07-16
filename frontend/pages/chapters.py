import uuid

from nicegui import ui

from frontend.components.chapters.chapter_content import ChapterContentComponent
from frontend.pages.base import BasePages

class ChapterPages(BasePages):
    def __init__(self):
        @ui.page("/chapters/read-id/{book_id}/{volume_number}/{chapter_number}")
        async def chapter_read_book_name(
            book_id: uuid.UUID,
            volume_number: int,
            chapter_number: int,
        ):
            await self.Header().render()

            await ChapterContentComponent(
                book_id=book_id,
                volume_number=volume_number,
                chapter_number=chapter_number,
            ).render()
