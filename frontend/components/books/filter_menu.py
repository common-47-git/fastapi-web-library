from nicegui import ui

from backend.src.users.endpoints import get_me
from backend.src.users_books import schemas as users_books_schemas
from frontend.components.books import (
    books_grid,
)


class FilterMenuComponent:
    def __init__(self, all_books: list):
        self.all_books = all_books
        self.selected_tags = set()
        self.grid_container = None
        self.menu_container = None

    def render(self):
        with ui.row().classes("w-full justify-center gap-10 px-4"):
            # Left: books grid container (takes majority of width)
            self.grid_container = ui.column().classes("w-7/10 items-center")

            # Right: filter menu container (narrower)
            self.menu_container = ui.column().classes("w-3/10 gap-4 p-4 pb-4 border border-gray-600 pb-1")

            # Inside the filter menu container: checkboxes
            with self.menu_container:
                for tag_name in sorted({tag.tag_name for book in self.all_books for tag in book.book_tags}):
                    def on_toggle(e, name=tag_name):
                        if e.value:
                            self.selected_tags.add(name)
                        else:
                            self.selected_tags.discard(name)
                        self._update_grid()

                    ui.checkbox(tag_name, on_change=on_toggle)

        self._update_grid()

    def _update_grid(self):
        if self.grid_container is None:
            return

        self.grid_container.clear()

        filtered_books = (
            [
                book
                for book in self.all_books
                if self.selected_tags.issubset({tag.tag_name for tag in book.book_tags})
            ]
            if self.selected_tags
            else self.all_books
        )

        with self.grid_container:
            books_grid.BooksGridComponent(books=filtered_books).render()
