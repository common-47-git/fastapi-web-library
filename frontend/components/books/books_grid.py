from nicegui import ui

from backend.src.books import schemas as books_schemas
from frontend.static import classes


class BooksGridComponent:
    def __init__(
        self,
        books: list[books_schemas.BookRead],
    ) -> None:
        self.books = books

    def render(self):
        with (
            ui.row()
            .classes(classes.BOOKS_GRID_CONTAINER)
        ):
            for book in self.books:
                self.BookCard(book).render()

    class BookCard:
        def __init__(self, book: books_schemas.BookRead) -> None:
            self.book = book

        def render(self):
            with ui.card().classes(classes.BOOK_CARD) as card:
                self.Image(self.book).render()
                self.Overlay(self.book).render()
                self.Navigation(card, self.book).bind()

        class Image:
            def __init__(self, book: books_schemas.BookRead) -> None:
                self.book = book

            def render(self):
                ui.image(self.book.book_cover).classes(classes.BOOK_CARD_IMG)

        class Overlay:
            def __init__(self, book: books_schemas.BookRead) -> None:
                self.book = book

            def render(self):
                with (
                    ui.row()
                    .classes(classes.BOOK_CARD_OVERLAY)
                    .style("background-color: rgba(0, 0, 0, 0.7);")
                ):
                    ui.label(self.book.book_name).classes(
                        classes.BOOK_CARD_LABEL,
                    )

        class Navigation:
            def __init__(
                self, card: ui.element, book: books_schemas.BookRead,
            ) -> None:
                self.card = card
                self.book = book

            def bind(self):
                self.card.on(
                    "click",
                    lambda _, book_id=self.book.book_id: ui.navigate.to(
                        f"/books/{book_id}",
                    ),
                )
