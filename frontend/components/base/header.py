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
            self.title = ui.label("📖 Books library").classes(classes.HEADER_SITE_TITLE)

            with ui.row(), ui.button(icon="menu"), ui.menu():
                ui.menu_item("BOOKS", lambda _: ui.navigate.to("/books"))
                if "access_token" not in app.storage.user:
                    ui.menu_item(
                        "LOG IN", lambda _: ui.navigate.to("/users/login"),
                    )
                else:
                    ui.menu_item("ME", lambda _: ui.navigate.to("/users/me"))
                    ui.menu_item("LOG OUT", lambda _: self._logout())


    def _logout(self):
        app.storage.user.clear()
        ui.notify("Logged out", color="warning")
        ui.navigate.to("/users/login")
