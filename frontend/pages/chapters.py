import uuid

from nicegui import ui

from frontend.components.chapters.chapter_content import render_chapter_content
from frontend.components.header import render_header


def add_chapters_pages():
    @ui.page("/chapters/read-id/{book_id}/{volume_number}/{chapter_number}")
    async def chapter_read_book_name(
        book_id: uuid.UUID,
        volume_number: int,
        chapter_number: int,
    ):
        await render_header()

        await render_chapter_content(
            book_id=book_id,
            volume_number=volume_number,
            chapter_number=chapter_number,
        )
