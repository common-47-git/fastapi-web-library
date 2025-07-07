from nicegui import ui


def render_book_cover(book):
    with ui.column():
        ui.image(book.book_cover).style(
            "width: 300px; height: 450px; object-fit: cover;",
        )
        ui.label(book.book_name).classes("text-3xl self-center")


def render_book_info(book, authors):
    with ui.column().classes("gap-2 max-w-2xl"):
        with ui.row():
            with ui.column():
                ui.label("Country: ").classes("text-base")
                ui.label("Release Date: ").classes("text-base")
                ui.label("Translation Status: ").classes("text-base")
                ui.label("Authors:").classes("text-base")

            with ui.column():
                ui.label(book.book_country).classes("text-base")
                ui.label(str(book.book_release_date)).classes("text-base")
                ui.label(book.book_translation_status.value).classes("text-base")

                with ui.row():
                    for author in authors:
                        full_name = f"{author.author_name} {author.author_surname}"
                        ui.link(
                            text=full_name,
                            target=f"/books/with-author/{author.author_id}",
                        ).classes("bg-sky-900 rounded px-2 text-base text-white no-underline")

        with ui.row().classes("p-2"):
            for tag in book.book_tags:
                ui.link(
                    text=tag.tag_name,
                    target=f"/books/with-tag/{tag.tag_id}",
                ).classes("bg-sky-900 rounded px-2 text-base text-white no-underline")

        ui.label(book.book_description).classes("text-base p-2").style("white-space: pre-wrap;")


