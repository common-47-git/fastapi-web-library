from enum import Enum
from nicegui import ui
from nicegui.events import EventArguments
from backend.src.books import schemas as books_schemas
from backend.src.enums import BookShelfEnum
from backend.src.users.models import UsersModel
from backend.src.users_books import schemas as users_books_schemas
from backend.src.users_books.endpoints import (
    patch_user_book_shelf,
    post_user_book,
)


async def _render_book_info_line(title: str, value: str | None) -> None:
    with ui.row().classes(
        "w-full justify-between border-b border-gray-600 pb-1"
    ):
        ui.label(title).classes("text-lg")
        ui.label(value or "Unknown").classes("text-lg")


async def _render_book_authors(title: str, authors: list | None) -> None:
    with ui.row().classes(
        "w-full justify-between border-b border-gray-600 pb-1",
    ):
        ui.label(title).classes("text-lg")
        if not authors:
            ui.label("Unknown").classes("text-lg")
        else:
            with ui.row().classes("flex-wrap gap-2"):
                for author in authors:
                    full_name = f"{author.author_name} {author.author_surname}"
                    ui.link(
                        text=full_name,
                        target=f"/books/with-author/{author.author_id}",
                    ).classes(
                        "bg-sky-900 rounded px-2 text-base text-white no-underline"
                    )


async def _render_book_tags(title: str, tags: list | None) -> None:
    if not tags:
        return
    with ui.row().classes("flex-wrap gap-2"):
        ui.label(title).classes("text-lg font-medium")
        for tag in tags:
            ui.link(
                text=tag.tag_name,
                target=f"/books/with-tag/{tag.tag_id}",
            ).classes(
                "bg-sky-900 rounded px-2 text-base text-white no-underline"
            )


async def _render_shelf_select(
    book: books_schemas.BookFullInfo,
    authed_user: UsersModel | None,
    current_book_shelf: Enum | None,
) -> None:
    shelf_options = [shelf.value for shelf in BookShelfEnum]

    # Default values (for unauthenticated users)
    selected_value = BookShelfEnum.TO_READ.value
    async def handle_unauthenticated(_: Enum) -> None:
        ui.notify("Log in first", color="primary")

    on_change_handler = handle_unauthenticated

    if authed_user:
        selected_value = current_book_shelf.value if current_book_shelf else None

        async def handle_update(e: Enum) -> None:
            selected = BookShelfEnum(e.value)
            await patch_user_book_shelf(
                users_books_schemas.UsersBooksUpdate(
                    user_id=authed_user.user_id,
                    book_id=book.book_id,
                    book_shelf=selected.value,
                ),
            )
            ui.notify(f"Moved to: {selected.value}", color="primary")

        async def handle_create(e: Enum) -> None:
            selected = BookShelfEnum(e.value)
            await post_user_book(
                users_books_schemas.UsersBooksCreate(
                    user_id=authed_user.user_id,
                    book_id=book.book_id,
                    book_shelf=selected.value,
                ),
            )
            ui.notify(f"Added to: {selected.value}", color="primary")

        on_change_handler = handle_update if current_book_shelf else handle_create

    ui.select(
        options=shelf_options,
        value=selected_value,
        on_change=on_change_handler,
    ).classes("w-full self-center")


async def _render_book_info_left(
    book: books_schemas.BookFullInfo,
    authed_user: UsersModel | None,
    current_book_shelf: Enum | None,
):
    with ui.column():
            ui.image(book.book_cover).style(
                "width: 250px; height: 400px; object-fit: cover;",
            )

            await _render_shelf_select(
                book,
                authed_user,
                current_book_shelf,
            )


async def _render_book_info_right(
    book: books_schemas.BookFullInfo,
):
    with ui.column().classes("gap-4 max-w-2xl"):
        ui.label(book.book_name).classes(
            "text-3xl self-center border-b border-gray-600 pb-1"
        )
        await _render_book_info_line(
            "🌍 Country",
            book.book_country,
        )
        await _render_book_info_line(
            "📅 Released",
            book.book_release_date.strftime("%d %b %Y").lstrip("0")
            if book.book_release_date
            else None,
        )
        await _render_book_info_line(
            "🈳 Translation",
            book.book_translation_status.value,
        )
        await _render_book_authors(
            "✍️ Authors",
            book.book_authors,
        )
        await _render_book_tags(
            "🏷️",
            book.book_tags,
        )
        ui.label(book.book_description or "No description").classes(
            "text-lg",
        ).style("white-space: pre-wrap;")


async def render_book_info(
    book: books_schemas.BookFullInfo,
    authed_user: UsersModel | None,
    current_book_shelf: Enum | None,
):
    with ui.row().classes("items-start justify-center gap-8 p-6 self-center"):
        await _render_book_info_left(
            book=book,
            authed_user=authed_user,
            current_book_shelf=current_book_shelf,
        )
        await _render_book_info_right(
            book=book,
        )



def render_books_grid(books: list[books_schemas.BookRead]):
    with ui.row().classes("flex flex-wrap gap-6 justify-center self-center"):
        for book in books:
            with ui.element("div").classes(
                "relative w-64 h-96 cursor-pointer group overflow-hidden rounded shadow-lg"
            ) as card:
                ui.image(book.book_cover).classes("w-full h-full object-cover")

                with (
                    ui.element("div")
                    .classes(
                        "absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 flex justify-center items-center"
                    )
                    .style("background-color: rgba(0, 0, 0, 0.7);")
                ):
                    ui.label(book.book_name).classes(
                        "text-white text-xl font-semibold text-center px-2"
                    )

                card.on(
                    "click",
                    lambda e, book_id=book.book_id: ui.navigate.to(
                        f"/books/{book_id}"
                    ),
                )
