from fastapi.security import OAuth2PasswordRequestForm
from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.users.endpoints import get_me, login_for_access_token
from frontend.components.header import render_header


def add_user_pages():
    @ui.page("/users/login")
    async def login_page():
        await render_header()
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
                        app.storage.user["access_token"] = (
                            token_data.access_token
                        )
                        ui.notify("Login successful")
                        ui.navigate.to("/users/me")
                    else:
                        ui.notify("Login failed", color="negative")
                except http_exceptions.NotFound404:
                    ui.notify("Wrong username or password(", color="negative")

            ui.button("Login", on_click=do_login).classes("w-full")

    @ui.page("/users/me")
    async def get_me_page():
        await render_header()
        jwt_token = app.storage.user["access_token"]

        current_user_schema = await get_me(jwt_token=jwt_token)

        with ui.card().classes("p-4 max-w-xl mx-auto mt-8"):
            ui.label(current_user_schema.username).classes(
                "text-2xl mb-4 font-bold self-center",
            )

            with ui.row().classes("w-full"):
                with ui.column().classes("items-end gap-2 text-right"):
                    ui.label("📧 Email:").classes("text-lg")
                    ui.label("📅 Registered:").classes("text-lg")

                with ui.column().classes("items-start gap-2"):
                    ui.label(current_user_schema.email).classes("text-lg")
                    ui.label(
                        str(current_user_schema.registration_date),
                    ).classes("text-lg")
        ui.button("Logout", on_click=logout).classes(
            "bg-red-600 text-white text-lg px-4 py-2 rounded-md hover:bg-red-700 transition",
        )


def logout():
    app.storage.user.clear()
    ui.notify("Logged out", color="warning")
    ui.navigate.to("/users/login")
