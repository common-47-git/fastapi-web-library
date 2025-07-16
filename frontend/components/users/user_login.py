from fastapi.security import OAuth2PasswordRequestForm
from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.users.endpoints import login_for_access_token
from backend.src.users.endpoints import post_user
from backend.src.users.schemas.users import UserCreate


class UserLoginComponent:
    def __init__(self):
        self.username_input = None
        self.password_input = None

    async def render(self):
        with ui.column().classes(
            "h-[87vh] items-center justify-center self-center"
        ):
            self.username_input = ui.input("Username").props("outlined")
            self.password_input = (
                ui.input("Password", password=True)
                .props("outlined")
                .props("toggle-password")
            )

            ui.button("Login", on_click=self.do_login).classes("w-full")

    async def do_login(self):
        try:
            # Спроба логіну
            token_data = await login_for_access_token(
                OAuth2PasswordRequestForm(
                    username=self.username_input.value,
                    password=self.password_input.value,
                ),
            )
            if token_data:
                app.storage.user["access_token"] = token_data.access_token
                ui.notify("Login successful")
                ui.navigate.to("/users/me")
            else:
                ui.notify("Login failed", color="negative")

        except http_exceptions.NotFound404:
            ui.notify("User not found. Registering...", color="warning")

            try:
                # Реєстрація нового користувача
                await post_user(
                    user=UserCreate(
                        username=self.username_input.value,
                        password=self.password_input.value,
                    )
                )
                ui.notify("User registered. Logging in...", color="primary")

                # Повтор логіну після успішної реєстрації
                token_data = await login_for_access_token(
                    OAuth2PasswordRequestForm(
                        username=self.username_input.value,
                        password=self.password_input.value,
                    )
                )
                app.storage.user["access_token"] = token_data.access_token
                ui.notify("Login successful")
                ui.navigate.to("/users/me")

            except http_exceptions.Conflict409:
                ui.notify("Username already exists. Try another.", color="negative")

            except Exception as e:
                ui.notify(f"Registration failed: {e}", color="negative")

