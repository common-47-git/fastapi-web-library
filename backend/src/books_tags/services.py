from backend.src import http_exceptions
from backend.src.books_tags import schemas as books_tags_schemas
from backend.src.books_tags.models import BooksTagsModel
from backend.src.books_tags.repository import BooksTagsRepository
from backend.src.services import BaseServices


class BooksTagsServices(BaseServices):
    alchemy_model: type[BooksTagsModel] = BooksTagsModel
    repository: type[BooksTagsRepository] = BooksTagsRepository

    async def read_books_tags_by_id(
        self,
        books_tags: books_tags_schemas.BooksTagsBase,
    ):
        return await BooksTagsRepository().read_books_tags_by_id(
            books_tags=books_tags,
        )

    async def delete_books_tags_by_id(
        self,
        books_tags: books_tags_schemas.BooksTagsDelete,
    ):
        deleted = await BooksTagsRepository().delete_books_tags_by_id(
            books_tags=books_tags,
        )
        if not deleted:
            raise http_exceptions.NotFound404
        return deleted
