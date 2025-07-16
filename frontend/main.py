from fastapi import FastAPI
from nicegui import ui

from backend.env.config import AuthConfig
from frontend.pages.books import BookPages
from frontend.pages.chapters import ChapterPages
from frontend.pages.users import UserPages


def init(fastapi_app: FastAPI) -> None:
    BookPages()
    UserPages()
    ChapterPages()

    ui.run_with(
        fastapi_app,
        mount_path="/gui",
        storage_secret=AuthConfig().SECRET_KEY,
        dark=True,
    )
