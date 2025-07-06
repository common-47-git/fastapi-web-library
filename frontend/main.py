import uuid
from pathlib import Path

from fastapi import FastAPI
from nicegui import app, ui

from backend.src.books.endpoints import books_all, books_get_by_id


def init(fastapi_app: FastAPI) -> None:
    static_dir = Path(__file__).parent / "static"
    app.add_static_files("frontend/static", static_dir)
    ui.add_head_html(
        "<link rel='stylesheet' type='text/css' href='/static/styles.css'>",
    )

    @ui.page("/")
    async def books() -> None:
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
            ui.image(book.book_cover).style(
                "width: 300px; height: 450px; object-fit: cover;",
            )

            # Right: Book Info
            with ui.column().classes("gap-2 max-w-2xl"):
                ui.label(book.book_name).style(
                    "font-size: 24px; font-weight: bold;",
                )
                # Country
                with ui.row():
                    ui.label("Country: ").style("font-size: 20px;")
                    ui.label(f"{book.book_country}").style("font-size: 18px;")

                # Release Date
                with ui.row():
                    ui.label("Release Date: ").style("font-size: 20px;")
                    ui.label(f"{book.book_release_date}").style(
                        "font-size: 18px;",
                    )

                # Translation Status
                with ui.row():
                    ui.label("Translation Status: ").style("font-size: 20px;")
                    ui.label(f"{book.book_translation_status.value}").style(
                        "font-size: 18px;",
                    )

                # Description
                with ui.row():
                    ui.label("Description: ").style("font-size: 20px;")
                    ui.label(f"{book.book_description}").style(
                        "font-size: 18px;",
                    )

                # Authors
                authors = [
                    f"{author.author_name} {author.author_surname}"
                    for author in book.book_authors
                    if author is not None
                ]
                with ui.row():
                    ui.label("Authors: ").style("font-size: 20px;")
                    ui.label(", ".join(authors)).style("font-size: 18px;")

                # Tags
                with ui.row():
                    ui.label("Tags: ").style("font-size: 20px;")
                    ui.label(
                        ", ".join([tag.tag_name for tag in book.book_tags]),
                    ).style("font-size: 18px;")

    ui.run_with(
        fastapi_app,
        storage_secret="st_sec",
    )
