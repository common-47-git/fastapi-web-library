from typing import Any

from nicegui import ui

from backend.src import http_exceptions


class LinkButtonComponent(ui.button):
    def __init__(
        self,
        link: str,
        response_detail: str | None = None,
        *args: tuple,
        **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(*args, **kwargs)
        self.link = link
        self.response_detail = response_detail
        self.on("click", self.navigate_to)
        self.link_exists = not isinstance(
            response_detail,
            http_exceptions.NotFound404,
        )

        if not self.link_exists:
            self.props("disabled")

    async def navigate_to(self) -> None:
        if self.link_exists:
            ui.navigate.to(self.link)
