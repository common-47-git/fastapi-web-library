from nicegui import ui

from backend.src.books import schemas as books_schemas
from backend.src.users_books import schemas as users_books_schemas


def render_books_grid(
    books: list[books_schemas.BookRead | users_books_schemas.UsersBooksRead],
):
    with ui.row().classes("flex flex-wrap gap-6 justify-center self-center"):
        for book in books:
            with ui.element("div").classes(
                "relative w-64 h-96 cursor-pointer group overflow-hidden rounded shadow-lg",
            ) as card:
                ui.image(book.book_cover).classes("w-full h-full object-cover")

                with (
                    ui.element("div")
                    .classes(
                        "absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 flex justify-center items-center",
                    )
                    .style("background-color: rgba(0, 0, 0, 0.7);")
                ):
                    ui.label(book.book_name).classes(
                        "text-white text-xl font-semibold text-center px-2",
                    )

                card.on(
                    "click",
                    lambda e, book_id=book.book_id: ui.navigate.to(
                        f"/books/{book_id}",
                    ),
                )
