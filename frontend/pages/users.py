from fastapi.security import OAuth2PasswordRequestForm
from nicegui import app, ui

from backend.src.users.endpoints import login_for_access_token, get_me
from backend.src.users.schemas import users as users_schemas

from frontend.static import classes, styles

def add_user_pages():
    @ui.page("/users/login")
    async def login_page():
        with ui.column().classes(
            "h-screen items-center justify-center self-center",
        ):
            username = ui.input("Username").props("outlined")
            password = (
                ui.input("Password", password=True)
                .props("outlined")
                .props("toggle-password")
            )

            async def do_login():
                token_data = await login_for_access_token(
                    OAuth2PasswordRequestForm(
                        username=username.value,
                        password=password.value,
                    ),
                )
                if token_data:
                    app.storage.user["access_token"] = token_data.access_token
                    ui.notify("Login successful")
                    ui.navigate.to("/books")
                else:
                    ui.notify("Login failed", color="negative")

            ui.button("Login", on_click=do_login).classes("w-full")

    @ui.page("/users/me")
    async def get_me_page():
        jwt_token = app.storage.user["access_token"]


        current_user_schema = await get_me(jwt_token=jwt_token)

        with ui.card().classes(classes.user_card):
            ui.label("👤 Current User Info").classes(
                "text-2xl mb-4 font-bold self-center",
            )

            with ui.row().classes("w-full"):
                with ui.column().classes("items-end gap-2 text-right"):
                    ui.label("👨 Username:").classes(classes.large_text)
                    ui.label("📧 Email:").classes(classes.large_text)
                    ui.label("📅 Registered:").classes(classes.large_text)

                with ui.column().classes("items-start gap-2"):
                    ui.label(current_user_schema.username).classes(classes.large_text)
                    ui.label(current_user_schema.email).classes(classes.large_text)
                    ui.label(
                        str(current_user_schema.registration_date).replace("-", " "),
                    ).classes(classes.large_text)

