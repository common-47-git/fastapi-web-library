import uuid

import httpx
from fastapi import FastAPI, status
from fastapi.security import OAuth2PasswordRequestForm
from nicegui import ui, app

from backend.src.books.endpoints import (
    get_all_books,
    get_book_by_id,
    get_books_with_author_id,
    get_books_with_tag_id,
)
from backend.src.users.endpoints import (
    login_for_access_token,
)
from frontend.components.books_grid import render_books_grid


def init(fastapi_app: FastAPI) -> None:
    @ui.page("/books")
    async def books() -> None:
        books = await get_all_books()
        render_books_grid(books=books)

    @ui.page("/books/{book_id}")
    async def books_id(book_id: uuid.UUID) -> None:
        book = await get_book_by_id(book_id=book_id)

        authors = [
            author for author in book.book_authors if author is not None
        ]

        with ui.row().classes("items-start justify-center gap-8 p-6"):
            # Book cover
            with ui.column():
                ui.image(book.book_cover).style(
                    "width: 300px; height: 450px; object-fit: cover;",
                )
                ui.label(book.book_name).classes("text-3xl self-center")

            # Book info
            with ui.column().classes("gap-2 max-w-2xl"):
                with ui.row():
                    with ui.column():
                        ui.label("Country: ").classes("text-base")
                        ui.label("Release Date: ").classes("text-base")
                        ui.label("Translation Status: ").classes("text-base")
                        ui.label("Authors:").classes("text-base")
                        ui.label("Tags:").classes("text-base")

                    with ui.column():
                        ui.label(book.book_country).classes("text-base")
                        ui.label(str(book.book_release_date)).classes(
                            "text-base",
                        )
                        ui.label(book.book_translation_status.value).classes(
                            "text-base",
                        )

                        with ui.row():
                            for author in authors:
                                full_name = f"{author.author_name} {author.author_surname}"
                                ui.link(
                                    text=full_name,
                                    target=f"/books/with-author/{author.author_id}",
                                ).classes(
                                    "bg-sky-900 rounded px-2 text-base text-white no-underline",
                                )

                        with ui.row():
                            for tag in book.book_tags:
                                ui.link(
                                    text=tag.tag_name,
                                    target=f"/books/with-tag/{tag.tag_id}",
                                ).classes(
                                    "bg-sky-900 rounded px-2 text-base text-white no-underline",
                                )

                # Description
                ui.label(book.book_description).classes("text-base").style(
                    "white-space: pre-wrap;",
                )

    @ui.page("/books/with-author/{author_id}")
    async def book_with_author_id(author_id: uuid.UUID) -> None:
        books = await get_books_with_author_id(author_id=author_id)
        render_books_grid(books=books)

    @ui.page("/books/with-tag/{tag_id}")
    async def book_with_tag_id(tag_id: uuid.UUID) -> None:
        books = await get_books_with_tag_id(tag_id=tag_id)
        render_books_grid(books=books)

    @ui.page("/login")
    async def login_page():
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

        login_btn = ui.button("Login", on_click=do_login)

    ui.run_with(
        fastapi_app,
        mount_path="/gui",
        storage_secret="st_sec",
        dark=True,
    )
