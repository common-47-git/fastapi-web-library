from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.enums import ModulesEnum
from backend.src.tags import schemas as tags_schemas
from backend.src.tags.models import TagsModel
from backend.src.tags.repository import TagsRepository

router = APIRouter(
    prefix=f"/{ModulesEnum.TAGS.value}",
    tags=[ModulesEnum.TAGS],
)


@router.get(
    "/all",
    response_model=list[tags_schemas.TagRead],
    summary="Get a list of tags.",
)
async def tags_all() -> Sequence[TagsModel]:
    """Get a list of tags with full info: id, name etc."""
    tags = await TagsRepository().read_all()
    if not tags:
        raise http_exceptions.NotFound404
    return tags


@router.post(
    "/add",
    response_model=tags_schemas.TagCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tag.",
)
async def tags_add(
    tag: tags_schemas.TagCreate,
):
    """Create a tag with properties specified in given schema."""
    try:
        return await TagsRepository.create_one(
            pydantic_schema=tag,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete(
    "/delete/{tag_id}",
    response_model=tags_schemas.TagDelete,
    summary="Delete a tag.",
)
async def tags_delete_by_id(
    tag_id: UUID,
) -> TagsModel:
    """Delete a tag by id."""
    deleted = await TagsRepository().delete_one_by_property(
        field_name=TagsModel.tag_id.key,
        field_value=tag_id,
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
