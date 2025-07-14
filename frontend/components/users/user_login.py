from fastapi.security import OAuth2PasswordRequestForm
from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.users.endpoints import login_for_access_token


async def render_user_login():
    with ui.column().classes(
        "h-[87vh] items-center justify-center self-center",
    ):
        username = ui.input("Username").props("outlined")
        password = (
            ui.input("Password", password=True)
            .props("outlined")
            .props("toggle-password")
        )

        async def do_login():
            try:
                token_data = await login_for_access_token(
                    OAuth2PasswordRequestForm(
                        username=username.value,
                        password=password.value,
                    ),
                )
                if token_data:
                    app.storage.user["access_token"] = token_data.access_token
                    ui.notify("Login successful")
                    ui.navigate.to("/users/me")
                else:
                    ui.notify("Login failed", color="negative")
            except http_exceptions.NotFound404:
                ui.notify("Wrong username or password(", color="negative")

        ui.button("Login", on_click=do_login).classes("w-full")
