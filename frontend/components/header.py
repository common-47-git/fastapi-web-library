from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.users.endpoints import get_me


class HeaderComponent:
    class LabelTitle:
        def render(self):
            ui.label("📖 Books library").classes("text-2xl font-bold")

    class NavLink:
        def __init__(self, text: str, target: str):
            self.text = text
            self.target = target
            self.classes = (
                "text-white text-lg font-medium px-4 py-2 rounded-md "
                "hover:bg-sky-700 hover:text-white transition duration-200 no-underline"
            )

        def render(self):
            ui.link(self.text, self.target).classes(self.classes)

    class LinksRow:
        def __init__(self):
            self.links = []

        def add_link(self, text: str, target: str):
            self.links.append(HeaderComponent.NavLink(text, target))

        def render(self):
            with ui.row().classes("gap-4 self-center"):
                for link in self.links:
                    link.render()

    def __init__(self):
        self.links_row = self.LinksRow()

    async def render(self):
        with ui.header().classes(
            "bg-transparent text-white px-9 py-4 border-b border-gray-600",
        ):
            with ui.row().classes("justify-between items-center w-full"):
                self.LabelTitle().render()

                self.links_row.add_link("📚 Books", "/books")
                if "access_token" not in app.storage.user:
                    self.links_row.add_link("Login", "/users/login")
                else:
                    try:
                        await get_me(
                            jwt_token=app.storage.user["access_token"],
                        )
                        self.links_row.add_link("🦲 Me", "/users/me")
                    except http_exceptions.Unauthorized401 as e:
                        self.logout()
                        ui.notify(f"Unauthorized {e}", color="warning")
                        return

                self.links_row.render()

    def logout(self):
        app.storage.user.clear()
        ui.notify("Logged out", color="warning")
        ui.navigate.to("/users/login")
