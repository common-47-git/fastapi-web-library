import uuid

from nicegui import ui

from backend.src.books import schemas as books_schemas


def render_book_info(book, authors):
    with ui.column():
        ui.image(book.book_cover).style(
            "width: 250px; height: 400px; object-fit: cover;",
        )
    with ui.column().classes("gap-4 max-w-2xl"):
        ui.label(book.book_name).classes(
            "text-3xl self-center border-b border-gray-600 pb-1",
        )
        with ui.row().classes(
            "w-full justify-between border-b border-gray-600 pb-1",
        ):
            ui.label("🌍 Country").classes("text-lg")
            ui.label(book.book_country if book.book_country else "Unknown").classes("text-lg")

        with ui.row().classes(
            "w-full justify-between border-b border-gray-600 pb-1",
        ):
            ui.label("📅 Released").classes("text-lg")
            ui.label(
                book.book_release_date.strftime("%d %b %Y").lstrip("0") if book.book_release_date else "Unknown",
            ).classes("text-lg")

        with ui.row().classes(
            "w-full justify-between border-b border-gray-600 pb-1",
        ):
            ui.label("🈳 Translation").classes("text-lg")
            ui.label(book.book_translation_status.value).classes("text-lg")

        with ui.row().classes(
            "w-full justify-between border-b border-gray-600 pb-1",
        ):
            ui.label("✍️ Authors").classes("text-lg")
            if book.book_authors == []:
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

        with ui.row().classes("flex-wrap gap-2"):
            if book.book_tags != []:
                ui.label("🏷️").classes("text-lg font-medium")
                for tag in book.book_tags:
                    ui.link(
                        text=tag.tag_name,
                        target=f"/books/with-tag/{tag.tag_id}",
                    ).classes(
                        "bg-sky-900 rounded px-2 text-base text-white no-underline",
                    )

        ui.label(book.book_description).classes("text-lg").style(
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
