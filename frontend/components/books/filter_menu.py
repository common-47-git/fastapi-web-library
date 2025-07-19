from nicegui import ui

from frontend.components.books import (
    books_grid,
)
from frontend.static import classes


class FilterMenuComponent:
    def __init__(self, all_books: list):
        self.all_books = all_books
        self.selected_tags = set()
        self.grid_container = None
        self.menu_container = None

    def render(self):
        with ui.row().classes(classes.FILTER_MENU_CONTAINER):
            # Left side: Grid container
            with ui.column().classes(
                classes.FILTER_MENU_GRID_CONTAINER,
            ) as self.grid_container:
                pass
            # Right side: Tag menu
            with ui.column().classes(
                classes.FILTER_MENU_TAGS_CONTAINER,
            ) as self.menu_container:
                for tag_name in sorted(
                    {
                        tag.tag_name
                        for book in self.all_books
                        for tag in book.book_tags
                    },
                ):

                    def _on_tag_toggle(e, name=tag_name):
                        if e.value:
                            self.selected_tags.add(name)
                        else:
                            self.selected_tags.discard(name)
                        self._update_grid()

                    ui.checkbox(tag_name, on_change=_on_tag_toggle)

        self._update_grid()

    def _update_grid(self):
        if self.grid_container is None:
            return

        self.grid_container.clear()

        filtered_books = (
            [
                book
                for book in self.all_books
                if self.selected_tags.issubset(
                    {tag.tag_name for tag in book.book_tags},
                )
            ]
            if self.selected_tags
            else self.all_books
        )

        with self.grid_container:
            books_grid.BooksGridComponent(books=filtered_books).render()
