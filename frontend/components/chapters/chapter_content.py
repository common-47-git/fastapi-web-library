import uuid

from nicegui import ui

from backend.src import http_exceptions
from backend.src.chapters.endpoints import get_chapter_by_book_id


class ChapterContentComponent:
    def __init__(
        self, book_id: uuid.UUID, volume_number: int, chapter_number: int,
    ) -> None:
        self.book_id = book_id
        self.volume_number = volume_number
        self.chapter_number = chapter_number
        self.chapter = None
        self.prev_exists = False
        self.next_exists = False

    async def _check_chapter_exists(self, chapter_number: int) -> bool:
        try:
            await get_chapter_by_book_id(
                self.book_id,
                self.volume_number,
                chapter_number,
            )
            return True
        except http_exceptions.NotFound404:
            return False

    async def _fetch_chapter(self) -> bool:
        try:
            self.chapter = await get_chapter_by_book_id(
                self.book_id,
                self.volume_number,
                self.chapter_number,
            )
        except http_exceptions.NotFound404:
            ui.navigate.to(f"/books/{self.book_id}")
            return False
        return True

    async def _check_nav_buttons(self) -> None:
        if self.chapter_number > 1:
            self.prev_exists = await self._check_chapter_exists(
                self.chapter_number - 1,
            )
        self.next_exists = await self._check_chapter_exists(
            self.chapter_number + 1,
        )

    def _render_header(self) -> None:
        ui.label(f"📖 {self.chapter.chapter_name}").classes(
            "text-2xl font-bold",
        )

    def _render_body(self) -> None:
        ui.label(self.chapter.chapter_content).classes("text-xl").style(
            "white-space: pre-wrap;",
        )

    def _render_nav_buttons(self) -> None:
        with ui.row().classes("self-center justify-center gap-4 mt-6"):
            # Prev button
            if self.prev_exists:
                ui.button(
                    "Prev",
                    on_click=lambda: ui.navigate.to(
                        f"/chapters/read-id/{self.book_id}/{self.volume_number}/{self.chapter_number - 1}",
                    ),
                ).classes("text-lg bg-sky-800 text-white")
            else:
                ui.button("Prev").classes("text-lg text-white").style(
                    "background-color: gray; cursor: not-allowed",
                ).props("disabled")

            ui.button(
                "📘 To Book",
                on_click=lambda: ui.navigate.to(f"/books/{self.book_id}"),
            ).classes("text-lg bg-gray-700 text-white")

            if self.next_exists:
                ui.button(
                    "Next",
                    on_click=lambda: ui.navigate.to(
                        f"/chapters/read-id/{self.book_id}/{self.volume_number}/{self.chapter_number + 1}",
                    ),
                ).classes("text-lg bg-sky-800 text-white")
            else:
                ui.button("Next").classes("text-lg text-white").style(
                    "background-color: gray; cursor: not-allowed",
                ).props("disabled")

    async def render(self):
        if not await self._fetch_chapter():
            return

        await self._check_nav_buttons()

        with (
            ui.column()
            .classes("self-center items-center gap-6")
            .style("width: 1024px")
        ):
            self._render_header()
            self._render_body()
            self._render_nav_buttons()
