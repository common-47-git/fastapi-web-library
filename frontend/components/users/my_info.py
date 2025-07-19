from nicegui import ui

from backend.src.users.schemas.users import UserRead
from frontend.components.base import info_line
from frontend.static import classes


class MyInfoComponent:
    def __init__(self, current_user: UserRead) -> None:
        self.current_user = current_user

    async def render(self):
        with ui.card().classes(classes.MY_INFO_CARD):
            await self.UsernameTitle(self.current_user.username).render()
            with ui.row().classes(classes.MY_INFO_ROW):
                await info_line.InfoLineComponent(
                    title="Email",
                    value=self.current_user.email,
                ).render()
                await info_line.InfoLineComponent(
                    title="Registered",
                    value=self.current_user.registration_date.strftime(
                        "%d %b %Y",
                    ).lstrip("0"),
                ).render()

    class UsernameTitle:
        def __init__(self, title: str) -> None:
            self.title = title

        async def render(self):
            ui.label(self.title).classes(classes.MY_INFO_USERNAME)
