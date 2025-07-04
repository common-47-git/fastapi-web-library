import uuid

from fastapi import FastAPI
from nicegui import ui

from backend.src.books.endpoints import books_all, books_get_by_id


def init(fastapi_app: FastAPI) -> None:
    @ui.page("/")
    async def show() -> None:
        ui.dark_mode().enable()

        books = await books_all()

        with ui.row().classes("w-full flex-wrap gap-4 justify-center"):
            for book in books:
                with ui.card().classes("cursor-pointer") as card:
                    ui.image(book.book_cover).style(
                        "width: 250px; height: 400px; object-fit: cover;",
                    )
                    ui.label(book.book_name).style("font-size: 18px;")
                    card.on(
                        "click",
                        lambda book=book: ui.navigate.to(
                            f"/book/{book.book_id}",
                        ),
                    )

    @ui.page("/book/{book_id}")
    async def book_detail(book_id: uuid.UUID) -> None:
        ui.dark_mode().enable()

        book = await books_get_by_id(book_id=book_id)

        with ui.row().classes("items-start justify-center gap-8 p-6"):
            # Left: Book Cover
            ui.image(book["book_cover"]).style(
                "width: 300px; height: 450px; object-fit: cover;",
            )

            # Right: Book Info
            with ui.column().classes("gap-2 max-w-2xl"):
                ui.label(book["book_name"]).style(
                    "font-size: 24px; font-weight: bold;",
                )
                ui.label(f"Country: {book['book_country']}")
                ui.label(f"Release Date: {book['book_release_date']}")
                ui.label(
                    f"Translation Status: {book['book_translation_status'].value}",
                )
                ui.label(f"Description: {book['book_description']}")
                authors = [
                    f"{author.author_name} {author.author_surname}"
                    for author in book["book_authors"]
                    if author is not None
                ]
                ui.label("Authors: " + ", ".join(authors))

                ui.label(
                    "Tags: "
                    + ", ".join(
                        [tag.tag_name for tag in book["book_tags"]],
                    ),
                )

    ui.run_with(
        fastapi_app,
        storage_secret="st_sec",
    )
