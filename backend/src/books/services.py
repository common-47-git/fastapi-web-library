import uuid
from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.books.models import BooksModel
from backend.src.books.repository import BooksRepository
from backend.src.database import BaseAlchemyModel
from backend.src.services import AbstractServices


class BooksServices(AbstractServices):
    async def create_one(self, pydantic_schema: BaseModel) -> BooksModel:
        try:
            return await BooksRepository().create_one(
                pydantic_schema=pydantic_schema,
            )
        except IntegrityError as e:
            raise http_exceptions.Conflict409(exception=e) from e

    async def read_one_by_property(
        self,
        property_name: str,
        property_value: Any,
    ) -> BooksModel | None:
        book = await BooksRepository().read_one_by_property(
            property_name=property_name,
            property_value=property_value,
        )
        if book is None:
            raise http_exceptions.NotFound404
        return book

    async def read_all(self) -> Sequence[BooksModel]:
        books = await BooksRepository().read_all()
        if not books:
            raise http_exceptions.NotFound404
        return books

    async def delete_one(
        self,
        book: BaseAlchemyModel,
    ) -> BooksModel:
        return await BooksRepository().delete_one(
            alchemy_model_to_delete=book,
        )

    async def delete_one_by_property(
        self,
        property_name: str,
        property_value: Any,
    ) -> BooksModel:
        return await BooksRepository().delete_one_by_property(
            property_name=property_name,
            property_value=property_value,
        )

    async def read_books_by_author_id(
        self,
        author_id: uuid.UUID,
    ) -> Sequence[BooksModel]:
        books = await BooksRepository().read_books_by_author_id(
            author_id=author_id,
        )
        if not books:
            raise http_exceptions.NotFound404
        return books
