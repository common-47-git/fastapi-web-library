import uuid

from backend.src import http_exceptions
from backend.src.chapters.models import ChaptersModel
from backend.src.chapters.repository import ChaptersRepository


async def chapter_exists_dep(chapter_id: uuid.UUID) -> ChaptersModel:
    chapter = await ChaptersRepository().read_one_by_property(
        property_name=ChaptersModel.chapter_id.key,
        property_value=chapter_id,
    )
    if chapter is None:
        raise http_exceptions.NotFound404
    return chapter

