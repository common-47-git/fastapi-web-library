from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.src import http_exceptions
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
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_all_tags():
    """Get a list of tags with full info: id, name etc."""
    return await TagsServices().read_all()


@router.post(
    "/add",
    response_model=tags_schemas.TagRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tag.",
    responses={
        201: http_exceptions.Created201().get_response_body(),
        409: http_exceptions.Conflict409().get_response_body(),
    },
)
async def post_tag(
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
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def delete_tag_by_id(
    existing_tag: Annotated[
        TagsModel,
        Depends(TagsDeps.one_exists),
    ], tag_id,
):
    """Delete a tag by id or raise 404."""
    return await TagsServices().delete_one(alchemy_object=existing_tag)
