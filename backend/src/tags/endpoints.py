from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.src.enums import ModulesEnum
from backend.src.tags import schemas as tags_schemas
from backend.src.tags.deps import TagsDeps
from backend.src.tags.models import TagsModel
from backend.src.tags.services import TagsServices

router = APIRouter(
    prefix=f"/{ModulesEnum.TAGS.value}",
    tags=[ModulesEnum.TAGS],
)


@router.get(
    "/",
    response_model=list[tags_schemas.TagRead],
    summary="Get a list of tags.",
)
async def tags_all():
    """Get a list of tags with full info: id, name etc."""
    return await TagsServices().read_all()


@router.post(
    "/add",
    response_model=tags_schemas.TagRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tag.",
)
async def tags_add(
    tag: tags_schemas.TagCreate,
):
    """Create a tag with properties specified in given schema."""
    return await TagsServices().create_one(
        pydantic_schema=tag,
    )


@router.delete(
    "/{tag_id}",
    response_model=tags_schemas.TagDelete,
    summary="Delete a tag.",
)
async def tags_delete_by_id(
    existing_tag: Annotated[
        TagsModel,
        Depends(TagsDeps.one_exists),
    ],
):
    """Delete a tag by id or raise 404."""
    return await TagsServices().delete_one(alchemy_object=existing_tag)
