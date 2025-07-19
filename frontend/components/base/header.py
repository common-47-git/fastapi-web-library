from nicegui import app, ui

from frontend.static import classes


class HeaderComponent(ui.header):
    def __init__(
        self,
        *,
        value: bool = True,
        fixed: bool = True,
        bordered: bool = False,
        elevated: bool = False,
        wrap: bool = True,
        add_scroll_padding: bool = True,
    ):
        super().__init__(
            value=value,
            fixed=fixed,
            bordered=bordered,
            elevated=elevated,
            wrap=wrap,
            add_scroll_padding=add_scroll_padding,
        )

        with self:
            self.title = ui.label("📖 Books library").classes(
                "flex max-sm:hidden text-2xl font-bold",
            )

            with ui.row().classes("flex max-sm:hidden"):
                ui.link("📚 Books", "/books").classes(classes.HEADER_NAV_LINK)
                if "access_token" not in app.storage.user:
                    ui.link("Login", "/users/login").classes(
                        classes.HEADER_NAV_LINK,
                    )
                else:
                    ui.link("🦲 Me", "/users/me").classes(
                        classes.HEADER_NAV_LINK,
                    )

            with ui.button(icon="menu").classes("flex sm:hidden"), ui.menu():
                ui.menu_item("Books", lambda _: ui.navigate.to("/books"))
                if "access_token" not in app.storage.user:
                    ui.menu_item(
                        "Login", lambda _: ui.navigate.to("/users/login"),
                    )
                else:
                    ui.menu_item("Me", lambda _: ui.navigate.to("/users/me"))
