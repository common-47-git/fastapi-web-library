from typing import Literal

from nicegui import ui

from frontend.static import classes


class InfoLineComponent(ui.row):
    def __init__(
        self,
        title: str,
        value: str | None,
        *,
        wrap: bool = True,
        align_items: Literal["start", "end", "center", "baseline", "stretch"]
        | None = None,
    ) -> None:
        super().__init__(wrap=wrap, align_items=align_items)
        self.title = title
        self.value = value
        with self.classes(classes.INFO_LINE_BORDER):
            self.title_label = ui.label(self.title).classes(classes.TEXT)
            self.value_label = ui.label(self.value or "Unknown").classes(
                classes.TEXT
            )
