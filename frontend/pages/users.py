from nicegui import app, ui

from backend.src.books.endpoints import get_books_with_user_id
from backend.src.users.endpoints import get_me
from backend.src.users_books import schemas as users_books_schemas
from frontend.components.header import render_header
from frontend.components.users.my_info import render_my_info
from frontend.components.users.user_login import render_user_login


def add_user_pages():
    @ui.page("/users/login")
    async def login_page():
        await render_header()
        await render_user_login()

    @ui.page("/users/me")
    async def get_me_page():
        await render_header()

        if "access_token" not in app.storage.user:
            ui.navigate.to("/users/login")
            return

        jwt_token = app.storage.user["access_token"]
        current_user = await get_me(jwt_token=jwt_token)
        books = await get_books_with_user_id(user_id=current_user.user_id)

        shelves = sorted(
            set(book.book_shelf for book in books if book.book_shelf)
        )
        default_shelf = shelves[0] if shelves else None

        await render_my_info(current_user=current_user)

        grid = render_books_grid_by_shelf(books=books, shelf=default_shelf)

        with ui.column().classes("self-center py-10"):
            ui.select(
                options=shelves,
                value=default_shelf,
                label="Choose shelf",
                on_change=lambda e: grid.refresh(books=books, shelf=e.value),
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
                    "relative w-64 h-96 cursor-pointer group overflow-hidden rounded shadow-lg",
                ) as card:
                    ui.image(book.book_cover).classes(
                        "w-full h-full object-cover"
                    )

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
    return render_books_grid_by_shelf
