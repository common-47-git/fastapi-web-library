from fastapi.security import OAuth2PasswordRequestForm
from nicegui import app, ui
from pydantic import ValidationError

from backend.src import http_exceptions
from backend.src.users.endpoints import login_for_access_token, post_user
from backend.src.users.schemas.users import UserCreate
from frontend.static import classes


class UserLoginComponent:
    def __init__(self):
        self.username_input = None
        self.password_input = None
        self.email_input = None
        self.register_checkbox = None

    async def render(self):
        with ui.column().classes(classes.LOGIN_CONTAINER):
            self.username_input = ui.input("Username").props("outlined")
            self.password_input = (
                ui.input("Password", password=True)
                .props("outlined")
                .props("toggle-password")
            )
            self.email_input = ui.input("Email").props("outlined")
            self.email_input.visible = False

            ui.button("Submit", on_click=self.do_submit).classes(
                classes.LOGIN_BUTTON,
            )

            self.register_checkbox = ui.checkbox(
                "Register",
                on_change=lambda e: setattr(
                    self.email_input,
                    "visible",
                    e.value,
                ),
            ).classes(classes.LOGIN_CHECKBOX)

    async def do_submit(self):
        if self.register_checkbox.value:
            # Registration flow
            if not self.email_input.value:
                ui.notify(
                    "Please enter an email to register",
                    color="negative",
                )
                return
            try:
                await post_user(
                    user=UserCreate(
                        username=self.username_input.value,
                        password=self.password_input.value,
                        email=self.email_input.value,
                    ),
                )
                ui.notify("User registered. Logging in...", color="primary")

                token_data = await login_for_access_token(
                    OAuth2PasswordRequestForm(
                        username=self.username_input.value,
                        password=self.password_input.value,
                    ),
                )
                app.storage.user["access_token"] = token_data.access_token
                ui.notify("Login successful")
                ui.navigate.to("/users/me")

            except http_exceptions.Conflict409 as conflict_e:
                ui.notify(
                    f"{conflict_e}".lstrip("409: "),
                    color="negative",
                )
            except ValidationError as e:
                messages = [error["msg"] for error in e.errors()]
                ui.notify("; ".join(messages), color="negative")

        else:
            # Login flow
            try:
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
                ui.notify("User not found. Please register.", color="warning")
            except http_exceptions.Unauthorized401:
                ui.notify(
                    "Unauthorized: Check your credentials.",
                    color="negative",
                )
            except ValidationError as e:
                messages = [error["msg"] for error in e.errors()]
                ui.notify("; ".join(messages), color="negative")
