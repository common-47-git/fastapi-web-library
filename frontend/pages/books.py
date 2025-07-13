import uuid

from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.books.endpoints import (
    get_all_books,
    get_book_by_id,
    get_books_with_author_id,
    get_books_with_tag_id,
)
from backend.src.users.endpoints import get_me
from backend.src.users_books import schemas as users_books_schemas
from backend.src.users_books.endpoints import get_user_book_by_id
from frontend.components.books import (
    render_book_info,
    render_books_grid,
)
from frontend.components.header import render_header


def add_books_pages():
    @ui.page("/books")
    async def books():
        await render_header()
        books = await get_all_books()
        render_books_grid(books=books)

    @ui.page("/books/{book_id}")
    async def books_id(book_id: uuid.UUID):
        await render_header()

        book = await get_book_by_id(book_id=book_id)

        token = app.storage.user.get("access_token")
        authed_user = await get_me(jwt_token=token) if token else None

        shelf = None
        if authed_user:
            try:
                user_book = await get_user_book_by_id(
                    users_books_schemas.UsersBooksBase(
                        user_id=authed_user.user_id,
                        book_id=book.book_id,
                    ),
                )
                shelf = user_book.book_shelf
            except http_exceptions.NotFound404:
                pass

        await render_book_info(
            book=book,
            authed_user=authed_user,
            current_book_shelf=shelf,
        )

    @ui.page("/books/with-author/{author_id}")
    async def book_with_author_id(author_id: uuid.UUID):
        await render_header()
        books = await get_books_with_author_id(author_id=author_id)
        render_books_grid(books=books)

    @ui.page("/books/with-tag/{tag_id}")
    async def book_with_tag_id(tag_id: uuid.UUID):
        await render_header()
        books = await get_books_with_tag_id(tag_id=tag_id)
        render_books_grid(books=books)
