from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.books.endpoints import get_books_with_user_id
from backend.src.users.endpoints import get_me
from backend.src.users_books import schemas as users_books_schemas
from frontend.components.users.my_info import MyInfoComponent
from frontend.components.users.user_login import UserLoginComponent
from frontend.pages.base import BasePages
from frontend.static import classes


class UserPages(BasePages):
    def __init__(self) -> None:
        @ui.page("/users/login")
        async def login_page() -> None:
            self.Header(fixed=False).classes(classes.HEADER_CONTAINER)
            await UserLoginComponent().render()

        @ui.page("/users/me")
        async def get_me_page() -> None:
            self.Header(fixed=False).classes(classes.HEADER_CONTAINER)

            if "access_token" not in app.storage.user:
                app.storage.user.clear()
                ui.navigate.to("/users/login")
                return
            current_user = None
            try:
                token = app.storage.user.get("access_token")
                current_user = await get_me(jwt_token=token) if token else None
            except http_exceptions.Unauthorized401:
                ui.navigate.to("/users/login")

            if current_user is None:
                app.storage.user.clear()
                ui.navigate.to("/users/login")
                return

            try:
                books = await get_books_with_user_id(
                    user_id=current_user.user_id,
                )
            except http_exceptions.NotFound404:
                books = []

            shelves = sorted(
                {book.book_shelf for book in books if book.book_shelf},
            )
            default_shelf = shelves[0] if shelves else None

            await MyInfoComponent(current_user=current_user).render()

            if not books:
                ui.label("YOU HAVE NOT ADDED ANY BOOKS (").classes(
                    "self-center text-3xl text-yellow-400 py-6",
                )
            else:
                grid = render_books_grid_by_shelf(
                    books=books,
                    shelf=default_shelf,
                )

                await self.ShelfSelectComponent(
                    shelves=shelves,
                    selected_shelf=default_shelf,
                    on_change=lambda shelf: grid.refresh(
                        books=books,
                        shelf=shelf,
                    ),
                ).render()

    class ShelfSelectComponent:
        def __init__(
            self,
            shelves: list[str],
            selected_shelf: str | None,
            on_change: callable,
        ) -> None:
            self.shelves = shelves
            self.selected_shelf = selected_shelf
            self.on_change = on_change

        async def render(self):
            with ui.column().classes("self-center"):
                ui.select(
                    options=self.shelves,
                    value=self.selected_shelf,
                    label="Choose shelf",
                    on_change=lambda e: self.on_change(e.value),
                ).classes("w-64 self-center")


@ui.refreshable
def render_books_grid_by_shelf(
    books: list[users_books_schemas.UsersBooksRead],
    shelf: str | None,
):
    with ui.row().classes("flex flex-wrap gap-6 justify-center self-center"):
        for book in books:
            if book.book_shelf == shelf:
                with ui.element("div").classes(
                        classes.BOOK_CARD,
                    ) as card:
                    ui.image(book.book_cover).classes(
                        "w-full h-full object-cover",
                    )
                    with (
                        ui.element("div").classes(
                            classes.BOOK_CARD_OVERLAY,
                        )
                        .style("background-color: rgba(0, 0, 0, 0.7);")
                    ):
                        ui.label(book.book_name).classes(
                            "text-white text-xl font-semibold text-center px-2",
                        )
                    card.on(
                        "click",
                        lambda _, book_id=book.book_id: ui.navigate.to(
                            f"/books/{book_id}",
                        ),
                    )
    return render_books_grid_by_shelf
