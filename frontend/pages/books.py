import uuid

from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.books.endpoints import (
    get_all_books_with_full_info,
    get_book_by_id,
    get_books_with_author_id,
    get_books_with_tag_id,
)
from backend.src.users.endpoints import get_me
from backend.src.users_books import schemas as users_books_schemas
from backend.src.users_books.endpoints import get_user_book_by_id
from frontend.components.books import book_info, books_grid, filter_menu
from frontend.pages.base import BasePages


class BookPages(BasePages):
    def __init__(self) -> None:
        @ui.page("/books")
        async def books() -> None:
            await self.Header().render()
            all_books = await get_all_books_with_full_info()
            filter_menu.FilterMenuComponent(all_books).render()

        @ui.page("/books/{book_id}")
        async def books_id(book_id: uuid.UUID) -> None:
            await self.Header().render()

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

            await book_info.BookInfoComponent(
                book=book,
                authed_user=authed_user,
                current_book_shelf=shelf,
            ).render()

        @ui.page("/books/with-author/{author_id}")
        async def book_with_author_id(author_id: uuid.UUID) -> None:
            await self.Header().render()
            books = await get_books_with_author_id(author_id=author_id)
            books_grid.BooksGridComponent(books=books).render()

        @ui.page("/books/with-tag/{tag_id}")
        async def book_with_tag_id(tag_id: uuid.UUID) -> None:
            await self.Header().render()
            books = await get_books_with_tag_id(tag_id=tag_id)
            books_grid.BooksGridComponent(books=books).render()
