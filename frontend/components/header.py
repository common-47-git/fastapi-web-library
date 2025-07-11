from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.users.endpoints import get_me


async def render_header():
    with ui.header().classes(
        "bg-transparent text-white px-9 py-4 border-b border-gray-600",
    ):
        with ui.row().classes("justify-between items-center w-full"):
            ui.label("📖 Books library").classes("text-2xl font-bold")

            with ui.row().classes("gap-4 self-center"):
                link_style = (
                    "text-white text-lg font-medium px-4 py-2 rounded-md "
                    "hover:bg-sky-700 hover:text-white transition duration-200 no-underline"
                )

                ui.link("📚 Books", "/books").classes(link_style)

                if "access_token" not in app.storage.user:
                    ui.link("Login", "/users/login").classes(link_style)
                else:
                    try:
                        await get_me(
                            jwt_token=app.storage.user["access_token"]
                        )
                        ui.link("🦲 Me", "/users/me").classes(link_style)
                    except http_exceptions.Unauthorized401 as e:
                        logout()
                        ui.notify(f"Unauthorized {e}", color="warning")
                        return


def logout():
    app.storage.user.clear()
    ui.notify("Logged out", color="warning")
    ui.navigate.to("/users/login")
