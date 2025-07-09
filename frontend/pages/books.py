import uuid

from nicegui import ui

from backend.src.books.endpoints import (
    get_all_books,
    get_book_by_id,
    get_books_with_author_id,
    get_books_with_tag_id,
)
from frontend.components.books import (
    render_book_cover,
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
        authors = [
            author for author in book.book_authors if author is not None
        ]
        with ui.row().classes(
            "items-start justify-center gap-8 p-6 self-center",
        ):
            render_book_cover(book)
            render_book_info(book, authors)

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
