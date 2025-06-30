import uuid

from backend.src import http_exceptions
from backend.src.services import BaseServices
from backend.src.tags.models import TagsModel
from backend.src.tags.repository import TagsRepository


class TagsServices(BaseServices):
    alchemy_model: type[TagsModel] = TagsModel
    repository: type[TagsRepository] = TagsRepository

    async def read_tags_by_book_id(
        self,
        book_id: uuid.UUID,
    ):
        entries = await TagsRepository().read_tags_by_book_id(book_id=book_id)
        if not entries:
            raise http_exceptions.NotFound404
        return entries
