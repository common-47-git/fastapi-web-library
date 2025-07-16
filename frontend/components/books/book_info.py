from enum import Enum

from nicegui import ui

from backend.src.books import schemas as books_schemas
from backend.src.enums import BookShelfEnum
from backend.src.users.models import UsersModel
from backend.src.users_books import schemas as users_books_schemas
from backend.src.users_books.endpoints import (
    patch_user_book_shelf,
    post_user_book,
)
from frontend.components import info_line


class BookInfoComponent:
    def __init__(
        self,
        book: books_schemas.BookFullInfo,
        authed_user: UsersModel | None,
        current_book_shelf: str | None,
    ) -> None:
        self.book = book
        self.authed_user = authed_user
        self.current_book_shelf = current_book_shelf

    async def render(self):
        with ui.row().classes(
            "items-start justify-center gap-8 pt-6 self-center",
        ):
            await self.Left(self).render()
            await self.Right(self).render()

    class Left:
        def __init__(self, parent: "BookInfoComponent") -> None:
            self.parent = parent

        async def render(self):
            with ui.column():
                await self.Image(self.parent).render()
                await BookInfoComponent.ShelfSelector(self.parent).render()
                await self.ReadButton(self.parent).render()

        class Image:
            def __init__(self, parent) -> None:
                self.book = parent.book

            async def render(self):
                ui.image(self.book.book_cover).style(
                    "width: 250px; height: 400px; object-fit: cover;",
                )

        class ReadButton:
            def __init__(self, parent) -> None:
                self.book = parent.book

            async def render(
                self,
                chapter_number: int = 1,
                volume_number: int = 1,
            ):
                ui.button(
                    "📖 Read",
                    on_click=lambda: ui.navigate.to(
                        f"/chapters/read-id/{self.book.book_id}/{volume_number}/{chapter_number}",
                    ),
                ).classes("w-full self-center bg-sky-900 text-lg rounded")

    class Right:
        def __init__(self, parent: "BookInfoComponent") -> None:
            self.parent = parent

        async def render(self):
            book = self.parent.book
            with ui.column().classes("gap-4 max-w-2xl"):
                BookInfoComponent.Right.Title(book.book_name).render()
                await info_line.InfoLineComponent(
                    "🌍 Country",
                    book.book_country,
                ).render()
                await info_line.InfoLineComponent(
                    "📅 Released",
                    book.book_release_date.strftime("%d %b %Y").lstrip("0")
                    if book.book_release_date
                    else None,
                ).render()
                await info_line.InfoLineComponent(
                    "🈳 Translation",
                    book.book_translation_status.value,
                ).render()
                await BookInfoComponent.Right.Authors(
                    book.book_authors,
                ).render()
                await BookInfoComponent.Right.Tags(book.book_tags).render()
                BookInfoComponent.Right.Description(
                    book.book_description,
                ).render()

        class Title:
            def __init__(self, title: str) -> None:
                self.title = title

            def render(self):
                ui.label(self.title).classes(
                    "text-3xl self-center border-b border-gray-600 pb-1",
                )

        class Description:
            def __init__(self, description: str | None) -> None:
                self.description = description or "No description"

            def render(self):
                ui.label(self.description).classes("text-lg").style(
                    "white-space: pre-wrap;",
                )

        class Authors:
            def __init__(self, authors: list | None) -> None:
                self.authors = authors

            async def render(self):
                with ui.row().classes(
                    "w-full justify-between border-b border-gray-600 pb-1",
                ):
                    ui.label("✍️ Authors").classes("text-lg")
                    if not self.authors:
                        ui.label("Unknown").classes("text-lg")
                    else:
                        with ui.row().classes("flex-wrap gap-2"):
                            for author in self.authors:
                                full_name = f"{author.author_name} {author.author_surname}"
                                ui.link(
                                    text=full_name,
                                    target=f"/books/with-author/{author.author_id}",
                                ).classes(
                                    "bg-sky-900 rounded px-2 text-base text-white no-underline",
                                )

        class Tags:
            def __init__(self, tags: list | None) -> None:
                self.tags = tags

            async def render(self):
                if not self.tags:
                    return
                with ui.row().classes("flex-wrap gap-2"):
                    ui.label("🏷️").classes("text-lg font-medium")
                    for tag in self.tags:
                        ui.link(
                            text=tag.tag_name,
                            target=f"/books/with-tag/{tag.tag_id}",
                        ).classes(
                            "bg-sky-900 rounded px-2 text-base text-white no-underline",
                        )

    class ShelfSelector:
        def __init__(self, parent: "BookInfoComponent") -> None:
            self.book_id = parent.book.book_id
            self.authed_user = parent.authed_user
            self.current_book_shelf = parent.current_book_shelf

        async def _handle_update(self, e: Enum) -> None:
            selected = BookShelfEnum(e.value)
            await patch_user_book_shelf(
                users_books_schemas.UsersBooksUpdate(
                    user_id=self.authed_user.user_id,
                    book_id=self.book_id,
                    book_shelf=selected.value,
                ),
            )
            ui.notify(f"Moved to: {selected.value}", color="primary")

        async def _handle_create(self, e: Enum) -> None:
            selected = BookShelfEnum(e.value)
            await post_user_book(
                users_books_schemas.UsersBooksCreate(
                    user_id=self.authed_user.user_id,
                    book_id=self.book_id,
                    book_shelf=selected.value,
                ),
            )
            ui.notify(f"Added to: {selected.value}", color="primary")

        async def _handle_unauthenticated(self, _: Enum) -> None:
            ui.notify("Log in first", color="primary")

        async def render(self):
            shelf_options = [shelf.value for shelf in BookShelfEnum]
            selected_value = None

            on_change_handler = self._handle_unauthenticated
            if self.authed_user:
                selected_value = (
                    self.current_book_shelf
                    if self.current_book_shelf
                    else None
                )
                on_change_handler = (
                    self._handle_update
                    if self.current_book_shelf
                    else self._handle_create
                )

            ui.select(
                options=shelf_options,
                value=selected_value,
                label="Choose shelf",
                on_change=on_change_handler,
            ).classes("w-full self-center")
