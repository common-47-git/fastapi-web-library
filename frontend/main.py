from fastapi import FastAPI
from nicegui import ui

from backend.env.config import AuthConfig
from frontend.pages.books import add_books_pages
from frontend.pages.users import add_user_pages


def init(fastapi_app: FastAPI) -> None:
    add_books_pages()
    add_user_pages()

    ui.run_with(
        fastapi_app,
        mount_path="/gui",
        storage_secret=AuthConfig().SECRET_KEY,
        dark=True,
    )
