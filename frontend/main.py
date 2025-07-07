import uuid

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from nicegui import app, ui
from backend.env.config import AuthConfig
from backend.src.books.endpoints import (
    get_all_books,
    get_book_by_id,
    get_books_with_author_id,
    get_books_with_tag_id,
)
from backend.src.users.endpoints import (
    login_for_access_token,
)
from backend.src.users.schemas import users as users_schemas
from backend.src.users.services import UsersServices
from frontend.components.books_grid import render_books_grid
from frontend.components.book_detail import render_book_cover, render_book_info


def init(fastapi_app: FastAPI) -> None:
    @ui.page("/books")
    async def books() -> None:
        books = await get_all_books()
        render_books_grid(books=books)

    @ui.page("/books/{book_id}")
    async def books_id(book_id: uuid.UUID) -> None:
        book = await get_book_by_id(book_id=book_id)
        authors = [author for author in book.book_authors if author is not None]
        with ui.row().classes("items-start justify-center gap-8 p-6"):
            render_book_cover(book)
            render_book_info(book, authors)

    @ui.page("/books/with-author/{author_id}")
    async def book_with_author_id(author_id: uuid.UUID) -> None:
        books = await get_books_with_author_id(author_id=author_id)
        render_books_grid(books=books)

    @ui.page("/books/with-tag/{tag_id}")
    async def book_with_tag_id(tag_id: uuid.UUID) -> None:
        books = await get_books_with_tag_id(tag_id=tag_id)
        render_books_grid(books=books)

    @ui.page("/users/login")
    async def login_page():
        with ui.column().classes("h-screen items-center justify-center self-center"):
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
        current_user_model = await UsersServices().read_current_user(
            token=jwt_token,
        )
        current_user_schema = users_schemas.UserRead.model_validate(
            current_user_model,
            from_attributes=True,
        )
        with ui.card().classes("p-4 max-w-xl mx-auto mt-8"):
                ui.label("👤 Current User Info").classes("text-2xl mb-4 font-bold self-center")

                with ui.row().classes("w-full"):
                    with ui.column().classes("items-end gap-2 text-right"):
                        ui.label("👨 Username:").classes("text-base")
                        ui.label("📧 Email:").classes("text-base")
                        ui.label("📅 Registered:").classes("text-base")
                        ui.label("🚫 Disabled:").classes("text-base")

                    with ui.column().classes("items-start gap-2"):
                        ui.label(current_user_schema.username).classes("text-base")
                        ui.label(current_user_schema.email).classes("text-base")
                        ui.label(str(current_user_schema.registration_date)).classes("text-base")
                        ui.label("Yes" if current_user_schema.disabled else "No").classes("text-base")

    ui.run_with(
        fastapi_app,
        mount_path="/gui",
        storage_secret=AuthConfig().SECRET_KEY,
        dark=True,
    )
