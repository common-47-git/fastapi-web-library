import uuid

from backend.src import http_exceptions
from backend.src.tags.models import TagsModel
from backend.src.tags.repository import TagsRepository


class TagsDeps:
    @staticmethod
    async def one_exists(tag_id: uuid.UUID) -> TagsModel:
        tag = await TagsRepository().read_one_by_property(
            property_name=TagsModel.tag_id.key,
            property_value=tag_id,
        )
        if tag is None:
            raise http_exceptions.NotFound404
        return tag
