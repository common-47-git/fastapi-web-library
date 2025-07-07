import uuid
from collections.abc import Sequence

from backend.src import http_exceptions
from backend.src.authors.models import AuthorsModel
from backend.src.authors.repository import AuthorsRepository
from backend.src.services import BaseServices


class AuthorsServices(BaseServices):
    alchemy_model: type[AuthorsModel] = AuthorsModel
    repository: type[AuthorsRepository] = AuthorsRepository

    async def read_authors_by_book_id(
        self,
        book_id: uuid.UUID,
    ) -> list[AuthorsModel] | None:
        authors = await self.repository().read_authors_by_book_id(
            book_id=book_id,
        )
        if authors is None:
            raise http_exceptions.NotFound404
        return authors
