from nicegui import ui


async def render_info_line(title: str, value: str | None) -> None:
    with ui.row().classes(
        "w-full justify-between border-b border-gray-600 pb-1",
    ):
        ui.label(title).classes("text-lg")
        ui.label(value or "Unknown").classes("text-lg")
