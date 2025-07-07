import uuid

from nicegui import ui

from backend.src.books import schemas as books_schemas


def render_books_grid(books: list[books_schemas.BookRead]):
    with ui.row().classes("w-full flex-wrap gap-4 justify-center"):
        for book in books:
            with ui.card().classes("cursor-pointer") as card:

                def go_to_detail(e, book_id: uuid.UUID = book.book_id):
                    ui.navigate.to(f"/books/{book_id}")

                ui.image(book.book_cover).style(
                    "width: 250px; height: 400px; object-fit: cover;",
                )
                ui.label(book.book_name).classes("text-base")
                card.on("click", go_to_detail)
