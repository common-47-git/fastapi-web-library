import uuid

from nicegui import ui

from backend.src import http_exceptions
from backend.src.chapters.endpoints import get_chapter_by_book_id


async def _check_chapter_exists(
    book_id: uuid.UUID,
    volume_number: int,
    chapter_number: int,
) -> bool:
    try:
        await get_chapter_by_book_id(book_id, volume_number, chapter_number)
        return True
    except http_exceptions.NotFound404:
        return False


def _render_chapter_header(chapter_name: str) -> None:
    ui.label(f"📖 {chapter_name}").classes("text-2xl font-bold")


def _render_chapter_body(content: str) -> None:
    ui.label(content).classes("text-xl").style("white-space: pre-wrap;")


def _render_chapter_nav_buttons(
    book_id: uuid.UUID,
    volume_number: int,
    chapter_number: int,
    prev_exists: bool,
    next_exists: bool,
) -> None:
    with ui.row().classes("self-center justify-center gap-4 mt-6"):
        # Prev button
        if prev_exists:
            ui.button(
                "Prev",
                on_click=lambda: ui.navigate.to(
                    f"/chapters/read-id/{book_id}/{volume_number}/{chapter_number - 1}",
                ),
            ).classes("text-lg bg-sky-800 text-white")
        else:
            ui.button("Prev").classes("text-lg text-white").style(
                "background-color: gray; cursor: not-allowed",
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
                "background-color: gray; cursor: not-allowed",
            ).props("disabled")


async def render_chapter_content(
    book_id: uuid.UUID,
    volume_number: int,
    chapter_number: int,
) -> None:
    try:
        chapter = await get_chapter_by_book_id(
            book_id,
            volume_number,
            chapter_number,
        )
    except http_exceptions.NotFound404:
        ui.navigate.to(f"/books/{book_id}")
        return

    prev_exists = (
        await _check_chapter_exists(book_id, volume_number, chapter_number - 1)
        if chapter_number > 1
        else False
    )
    next_exists = await _check_chapter_exists(
        book_id,
        volume_number,
        chapter_number + 1,
    )

    with (
        ui.column()
        .classes("self-center items-center gap-6")
        .style("width: 1024px")
    ):
        _render_chapter_header(chapter.chapter_name)
        _render_chapter_body(chapter.chapter_content)
        _render_chapter_nav_buttons(
            book_id,
            volume_number,
            chapter_number,
            prev_exists,
            next_exists,
        )
