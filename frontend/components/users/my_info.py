from nicegui import ui

from backend.src.users.schemas.users import UserRead
from frontend.components.base import info_line
from frontend.static import classes


class MyInfoComponent:
    def __init__(self, current_user: UserRead) -> None:
        self.current_user = current_user

    async def render(self):
        with ui.card().classes(classes.MY_INFO_CARD):
            self.username_title = ui.label(self.current_user.username).classes(
                classes.MY_INFO_USERNAME
            )
            with ui.row().classes(classes.MY_INFO_ROW):
                info_line.InfoLineComponent(
                    title="Email",
                    value=self.current_user.email,
                )
                info_line.InfoLineComponent(
                    title="Registered",
                    value=self.current_user.registration_date.strftime(
                        "%d %b %Y",
                    ).lstrip("0"),
                )
