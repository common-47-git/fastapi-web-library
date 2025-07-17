from nicegui import ui
from frontend.static import classes

class InfoLineComponent:
    class LabelTitle:
        def __init__(self, text: str) -> None:
            self.text = text

        def render(self):
            ui.label(self.text).classes(classes.TEXT)

    class LabelValue:
        def __init__(self, value: str | None) -> None:
            self.value = value or "Unknown"

        def render(self):
            ui.label(self.value).classes(classes.TEXT)

    def __init__(self, title: str, value: str | None) -> None:
        self.title = title
        self.value = value

    async def render(self) -> None:
        with ui.row().classes(classes.INFO_LINE_BORDER):
            self.LabelTitle(self.title).render()
            self.LabelValue(self.value).render()
