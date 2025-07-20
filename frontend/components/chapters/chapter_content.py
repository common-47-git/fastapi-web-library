import uuid

from nicegui import ui

from backend.src import http_exceptions
from backend.src.chapters.endpoints import get_chapter_by_book_id
from frontend.components.base.link_button import LinkButtonComponent
from frontend.static import classes


class ChapterContentComponent:
    def __init__(
        self,
        book_id: uuid.UUID,
        volume_number: int,
        chapter_number: int,
    ) -> None:
        self.book_id = book_id
        self.volume_number = volume_number
        self.chapter_number = chapter_number
        self.chapter = None
        self.prev_exists = False
        self.next_exists = False

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

    def _render_header(self) -> None:
        ui.label(f"📖 {self.chapter.chapter_name}").classes(
            classes.CHAPTER_HEADER,
        )

    def _render_body(self) -> None:
        ui.label(self.chapter.chapter_content).classes(
            classes.CHAPTER_BODY,
        ).style(
            "white-space: pre-wrap;",
        )

    async def _render_nav_buttons(self) -> None:
        with ui.row().classes(classes.CHAPTER_NAV_ROW):
            try:
                resp = await get_chapter_by_book_id(
                    self.book_id,
                    self.volume_number,
                    self.chapter_number - 1,
                )
            except http_exceptions.APIException as e:
                resp = e

            LinkButtonComponent(
                text="Prev",
                link=f"/chapters/read-id/{self.book_id}/{self.volume_number}/{self.chapter_number - 1}",
                response_detail=resp,
            ).classes(classes.CHAPTER_NAV_BUTTON)

            LinkButtonComponent(
                text="To Book",
                link=f"/books/{self.book_id}",
            ).classes(classes.CHAPTER_BACK_TO_BOOK)

            try:
                resp = await get_chapter_by_book_id(
                    self.book_id,
                    self.volume_number,
                    self.chapter_number + 1,
                )
            except http_exceptions.APIException as e:
                resp = e

            LinkButtonComponent(
                text="Next",
                link=f"/chapters/read-id/{self.book_id}/{self.volume_number}/{self.chapter_number + 1}",
                response_detail=resp,
            ).classes(classes.CHAPTER_NAV_BUTTON)

    async def render(self):
        if not await self._fetch_chapter():
            return

        with ui.column().classes(
            classes.CHAPTER_CONTENT_CONTAINER,
        ):
            self._render_header()
            self._render_body()
            await self._render_nav_buttons()
