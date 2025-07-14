from nicegui import app, ui

from backend.src.users.schemas.users import UserRead
from frontend.components import info_line


async def _render_username_as_title(title: str) -> None:
    ui.label(title).classes(
        "text-3xl self-center border-b border-gray-600 pb-1",
    )


async def render_my_info(current_user: UserRead):
    with ui.card().classes("p-4 max-w-xl mx-auto mt-8"):
        await _render_username_as_title(title=current_user.username)
        with ui.row().classes("w-full"):
            await info_line.render_info_line(
                title="Email",
                value=current_user.email,
            )
            await info_line.render_info_line(
                title="Registered",
                value=current_user.registration_date.strftime(
                    "%d %b %Y",
                ).lstrip("0"),
            )
        ui.button("Logout", on_click=logout).classes(
            "self-center bg-red-600 text-white text-lg px-4 py-2 rounded-md hover:bg-red-700 transition",
        )


def logout():
    app.storage.user.clear()
    ui.notify("Logged out", color="warning")
    ui.navigate.to("/users/login")
