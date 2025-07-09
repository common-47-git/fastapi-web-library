import uuid

from nicegui import ui

from backend.src.books import schemas as books_schemas
from frontend.static import classes, styles


def render_book_cover(book):
    with ui.column():
        ui.image(book.book_cover).style(
            styles.book_cover,
        )
        ui.label(book.book_name).classes("text-3xl self-center")


def render_book_info(book, authors):
    with ui.column().classes("gap-2 max-w-2xl"):
        with ui.row():
            with ui.column():
                ui.label("Country: ").classes(classes.large_text)
                ui.label("Release Date: ").classes(classes.large_text)
                ui.label("Translation Status: ").classes(classes.large_text)
                ui.label("Authors:").classes(classes.large_text)

            with ui.column():
                ui.label(book.book_country).classes(classes.large_text)
                ui.label(str(book.book_release_date)).classes(
                    classes.large_text,
                )
                ui.label(book.book_translation_status.value).classes(
                    classes.large_text,
                )

                with ui.row():
                    for author in authors:
                        full_name = (
                            f"{author.author_name} {author.author_surname}"
                        )
                        ui.link(
                            text=full_name,
                            target=f"/books/with-author/{author.author_id}",
                        ).classes(classes.blue_link_box)

        with ui.row():
            for tag in book.book_tags:
                ui.link(
                    text=tag.tag_name,
                    target=f"/books/with-tag/{tag.tag_id}",
                ).classes(classes.blue_link_box)

        ui.label(book.book_description).classes(classes.large_text).style("white-space: pre-wrap;")


def render_books_grid(books: list[books_schemas.BookRead]):
    with ui.row().classes("flex flex-wrap gap-6 justify-center self-center"):
        for book in books:
            with ui.element("div").classes(classes.book_card) as card:

                def go_to_detail(e, book_id: uuid.UUID = book.book_id):
                    ui.navigate.to(f"/books/{book_id}")

                ui.image(book.book_cover).classes("w-full h-full object-cover")

                with ui.element("div").classes(classes.book_name_hover).style(styles.book_name_hover_transparency):
                    ui.label(book.book_name).classes(classes.book_name_label)

                card.on("click", go_to_detail)


