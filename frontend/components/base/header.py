from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.users.endpoints import get_me
from frontend.static import classes


class HeaderComponent:
    class LabelTitle:
        def render(self) -> None:
            ui.label("📖 Books library").classes(classes.HEADER_SITE_TITLE)

    class NavLink:
        def __init__(self, text: str, target: str) -> None:
            self.text = text
            self.target = target

        def render(self) -> None:
            ui.link(self.text, self.target).classes(classes.HEADER_NAV_LINK)

    class LinksRow:
        def __init__(self) -> None:
            self.links = []

        def add_link(self, text: str, target: str) -> None:
            self.links.append(HeaderComponent.NavLink(text, target))

        def render(self) -> None:
            with ui.row().classes("gap-4 self-center"):
                for link in self.links:
                    link.render()

    def __init__(self) -> None:
        self.links_row = self.LinksRow()

    async def render(self) -> None:
        with (
            ui.header().classes(classes.HEADER_CONTAINER),
            ui.row().classes(classes.HEADER_ROW),
        ):
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

    def logout(self) -> None:
        app.storage.user.clear()
        ui.notify("Logged out", color="warning")
        ui.navigate.to("/users/login")


