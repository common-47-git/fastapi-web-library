from nicegui import app, ui

from backend.src.users.schemas.users import UserRead
from frontend.components import info_line


class MyInfoComponent:
    def __init__(self, current_user: UserRead):
        self.current_user = current_user

    async def render(self):
        with ui.card().classes("p-4 max-w-xl mx-auto mt-8"):
            await self.UsernameTitle(self.current_user.username).render()
            with ui.row().classes("w-full"):
                await info_line.InfoLineComponent(
                    title="Email",
                    value=self.current_user.email,
                ).render()
                await info_line.InfoLineComponent(
                    title="Registered",
                    value=self.current_user.registration_date.strftime(
                        "%d %b %Y"
                    ).lstrip("0"),
                ).render()
            ui.button("Logout", on_click=self.logout).classes(
                "self-center bg-red-600 text-white text-lg px-4 py-2 rounded-md hover:bg-red-700 transition",
            )

    class UsernameTitle:
        def __init__(self, title: str):
            self.title = title

        async def render(self):
            ui.label(self.title).classes(
                "text-3xl self-center border-b border-gray-600 pb-1",
            )

    def logout(self):
        app.storage.user.clear()
        ui.notify("Logged out", color="warning")
        ui.navigate.to("/users/login")
