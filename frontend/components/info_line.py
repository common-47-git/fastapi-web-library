from nicegui import ui


class InfoLineComponent:
    class LabelTitle:
        def __init__(self, text: str):
            self.text = text

        def render(self):
            ui.label(self.text).classes("text-lg")

    class LabelValue:
        def __init__(self, value: str | None):
            self.value = value or "Unknown"

        def render(self):
            ui.label(self.value).classes("text-lg")

    def __init__(self, title: str, value: str | None):
        self.title = title
        self.value = value

    async def render(self):
        with ui.row().classes(
            "w-full justify-between border-b border-gray-600 pb-1",
        ):
            self.LabelTitle(self.title).render()
            self.LabelValue(self.value).render()
