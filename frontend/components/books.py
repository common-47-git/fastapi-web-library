import uuid

from nicegui import app, ui

from backend.src import http_exceptions
from backend.src.books import schemas as books_schemas
from backend.src.enums import BookShelfEnum
from backend.src.users.endpoints import get_me
from backend.src.users_books import schemas as users_books_schemas
from backend.src.users_books.endpoints import (
    get_user_book_by_id,
    patch_user_book_shelf,
    post_user_book,
)


async def _render_book_info_line(title: str, value: str | None) -> None:
    with ui.row().classes(
        "w-full justify-between border-b border-gray-600 pb-1",
    ):
        ui.label(title).classes("text-lg")
        ui.label(value if value else "Unknown").classes("text-lg")


async def _render_book_authors(title: str, authors: list | None) -> None:
    with ui.row().classes(
        "w-full justify-between border-b border-gray-600 pb-1",
    ):
        ui.label(title).classes("text-lg")
        if authors == [] or authors is None:
            ui.label("Unknown").classes("text-lg")
        else:
            with ui.row().classes("flex-wrap gap-2"):
                for author in authors:
                    full_name = f"{author.author_name} {author.author_surname}"
                    ui.link(
                        text=full_name,
                        target=f"/books/with-author/{author.author_id}",
                    ).classes(
                        "bg-sky-900 rounded px-2 text-base text-white no-underline",
                    )


async def _render_book_tags(title: str, tags: list | None) -> None:
    with ui.row().classes("flex-wrap gap-2"):
        if tags != [] and tags is not None:
            ui.label(title).classes("text-lg font-medium")
            for tag in tags:
                ui.link(
                    text=tag.tag_name,
                    target=f"/books/with-tag/{tag.tag_id}",
                ).classes(
                    "bg-sky-900 rounded px-2 text-base text-white no-underline",
                )


async def render_book_info(book: books_schemas.BookFullInfo):
    with ui.column():
        ui.image(book.book_cover).style(
            "width: 250px; height: 400px; object-fit: cover;",
        )

        try:
            if "access_token" not in app.storage.user:
                raise http_exceptions.Unauthorized401

            me = await get_me(jwt_token=app.storage.user["access_token"])

            try:
                user_book = await get_user_book_by_id(
                    user_book=users_books_schemas.UsersBooksBase(
                        user_id=me.user_id,
                        book_id=book.book_id,
                    ),
                )

                if user_book.book_shelf:

                    async def on_shelf_change(shelf):
                        await patch_user_book_shelf(
                            users_books_schemas.UsersBooksUpdate(
                                user_id=me.user_id,
                                book_id=book.book_id,
                                book_shelf=shelf.value,
                            )
                        )
                        ui.notify(f"Moved to: {shelf.value}", color="primary")

                    ui.select(
                        [shelf.value for shelf in BookShelfEnum],
                        value=BookShelfEnum[user_book.book_shelf.name].value,
                        on_change=on_shelf_change,
                    ).classes("w-full self-center")
            except http_exceptions.NotFound404:

                async def on_shelf_create(shelf):
                    await post_user_book(
                        users_books_schemas.UsersBooksCreate(
                            user_id=me.user_id,
                            book_id=book.book_id,
                            book_shelf=shelf.value,
                        ),
                    )
                    ui.notify(f"Added to: {shelf.value}", color="primary")

                ui.select(
                    [shelf.value for shelf in BookShelfEnum],
                    value=None,
                    on_change=on_shelf_create,
                ).classes("w-full self-center")

        except http_exceptions.Unauthorized401:
            with ui.row().classes("w-full items-center gap-3"):
                ui.select(
                    [shelf.value for shelf in BookShelfEnum],
                    value=BookShelfEnum.TO_READ,
                    on_change=lambda e: ui.notify(
                        "Log in first",
                        color="primary",
                    ),
                ).classes("w-full self-center")

    with ui.column().classes("gap-4 max-w-2xl"):
        ui.label(book.book_name).classes(
            "text-3xl self-center border-b border-gray-600 pb-1",
        )

        await _render_book_info_line(
            title="🌍 Country",
            value=book.book_country,
        )

        await _render_book_info_line(
            title="📅 Released",
            value=book.book_release_date.strftime("%d %b %Y").lstrip("0")
            if book.book_release_date
            else None,
        )

        await _render_book_info_line(
            title="🈳 Translation",
            value=book.book_translation_status.value,
        )

        await _render_book_authors(
            title="✍️ Authors",
            authors=book.book_authors,
        )

        await _render_book_tags(
            title="🏷️",
            tags=book.book_tags,
        )

        ui.label(
            book.book_description
            if book.book_description
            else "No description",
        ).classes("text-lg").style(
            "white-space: pre-wrap;",
        )


def render_books_grid(books: list[books_schemas.BookRead]):
    with ui.row().classes("flex flex-wrap gap-6 justify-center self-center"):
        for book in books:
            with ui.element("div").classes(
                "relative w-64 h-96 cursor-pointer group overflow-hidden rounded shadow-lg",
            ) as card:

                def go_to_detail(e, book_id: uuid.UUID = book.book_id):
                    ui.navigate.to(f"/books/{book_id}")

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

                card.on("click", go_to_detail)
