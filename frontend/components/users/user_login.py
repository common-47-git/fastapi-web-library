from fastapi.security import OAuth2PasswordRequestForm
from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.users.endpoints import login_for_access_token


class UserLoginComponent:
    def __init__(self):
        self.username_input = None
        self.password_input = None

    async def render(self):
        with ui.column().classes("h-[87vh] items-center justify-center self-center"):
            self.username_input = ui.input("Username").props("outlined")
            self.password_input = (
                ui.input("Password", password=True)
                .props("outlined")
                .props("toggle-password")
            )

            ui.button("Login", on_click=self.do_login).classes("w-full")

    async def do_login(self):
        try:
            token_data = await login_for_access_token(
                OAuth2PasswordRequestForm(
                    username=self.username_input.value,
                    password=self.password_input.value,
                )
            )
            if token_data:
                app.storage.user["access_token"] = token_data.access_token
                ui.notify("Login successful")
                ui.navigate.to("/users/me")
            else:
                ui.notify("Login failed", color="negative")
        except http_exceptions.NotFound404:
            ui.notify("Wrong username or password(", color="negative")
