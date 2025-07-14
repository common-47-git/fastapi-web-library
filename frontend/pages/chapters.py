import uuid

from nicegui import ui

from backend.src import http_exceptions
from backend.src.chapters.endpoints import (
    get_chapter_by_book_id,
)
from frontend.components.header import render_header


def add_chapters_pages():
    @ui.page("/chapters/read-id/{book_id}/{volume_number}/{chapter_number}")
    async def chapter_read_book_name(
        book_id: uuid.UUID, volume_number: int, chapter_number: int
    ):
        await render_header()

        try:
            chapter = await get_chapter_by_book_id(
                book_id=book_id,
                volume_number=volume_number,
                chapter_number=chapter_number,
            )
        except http_exceptions.NotFound404:
            ui.navigate.to(f"/books/{book_id}")
            return

        prev_exists = False
        if chapter_number > 1:
            try:
                await get_chapter_by_book_id(
                    book_id=book_id,
                    volume_number=volume_number,
                    chapter_number=chapter_number - 1,
                )
                prev_exists = True
            except http_exceptions.NotFound404:
                pass

        next_exists = False
        try:
            await get_chapter_by_book_id(
                book_id=book_id,
                volume_number=volume_number,
                chapter_number=chapter_number + 1,
            )
            next_exists = True
        except http_exceptions.NotFound404:
            pass

        with (
            ui.column()
            .classes("self-center items-center gap-6")
            .style("width: 1024px")
        ):
            # Chapter title
            ui.label(f"📖 {chapter.chapter_name}").classes("text-2xl font-bold")

            # Chapter content
            ui.label(chapter.chapter_content).classes("text-xl").style(
                "white-space: pre-wrap;"
            )

            with ui.row().classes("self-center justify-center gap-4 mt-6"):

                if prev_exists:
                    ui.button(
                        "Prev",
                        on_click=lambda: ui.navigate.to(
                            f"/chapters/read-id/{book_id}/{volume_number}/{chapter_number - 1}",
                        ),
                    ).classes("text-lg bg-sky-800 text-white")
                else:
                    ui.button("Prev").classes("text-lg text-white").style(
                        "background-color: gray; cursor: not-allowed"
                    ).props("disabled")

                ui.button(
                    "📘 To Book",
                    on_click=lambda: ui.navigate.to(f"/books/{book_id}"),
                ).classes("text-lg bg-gray-700 text-white")

                if next_exists:
                    ui.button(
                        "Next",
                        on_click=lambda: ui.navigate.to(
                            f"/chapters/read-id/{book_id}/{volume_number}/{chapter_number + 1}",
                        ),
                    ).classes("text-lg bg-sky-800 text-white")
                else:
                    ui.button("Next").classes("text-lg text-white").style(
                        "background-color: gray; cursor: not-allowed"
                    ).props("disabled")

