from nicegui import ui
from backend.src.books import schemas as books_schemas


class BooksGridComponent:
    def __init__(
        self,
        books: list[books_schemas.BookRead],
    ):
        self.books = books

    def render(self):
        with ui.row().classes("flex flex-wrap gap-6 justify-center self-center"):
            for book in self.books:
                self.BookCard(book).render()

    class BookCard:
        def __init__(self, book: books_schemas.BookRead):
            self.book = book

        def render(self):
            with ui.card().classes(
                "relative w-64 h-96 cursor-pointer group overflow-hidden rounded shadow-lg p-0"
            ) as card:
                self.Image(self.book).render()
                self.Overlay(self.book).render()
                self.Navigation(card, self.book).bind()

        class Image:
            def __init__(self, book: books_schemas.BookRead):
                self.book = book

            def render(self):
                ui.image(self.book.book_cover).classes("w-full h-full object-cover")

        class Overlay:
            def __init__(self, book: books_schemas.BookRead):
                self.book = book

            def render(self):
                with ui.row().classes(
                    "absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 justify-center items-center"
                ).style("background-color: rgba(0, 0, 0, 0.7);"):
                    ui.label(self.book.book_name).classes(
                        "text-white text-xl font-semibold text-center px-2"
                    )

        class Navigation:
            def __init__(self, card: ui.element, book: books_schemas.BookRead):
                self.card = card
                self.book = book

            def bind(self):
                self.card.on(
                    "click",
                    lambda _, book_id=self.book.book_id: ui.navigate.to(
                        f"/books/{book_id}",
                    ),
                )
