from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import crud, http_exceptions
from backend.src.database import async_session_dependency
from backend.src.enums import ModulesEnum
from backend.src.tags import schemas as tags_schemas
from backend.src.tags.models import TagsModel

router = APIRouter(
    prefix=f"/{ModulesEnum.TAGS.value}",
    tags=[ModulesEnum.TAGS],
)


@router.get("/all", response_model=list[tags_schemas.TagRead])
async def tags_all(
    session: async_session_dependency,
) -> Sequence[TagsModel]:
    tags = await crud.read_entities(alchemy_model=TagsModel, session=session)
    if not tags:
        raise http_exceptions.NotFound404
    return tags


@router.post(
    "/add",
    response_model=tags_schemas.TagCreate,
    status_code=status.HTTP_201_CREATED,
)
async def tags_add(
    session: async_session_dependency,
    tag: tags_schemas.TagCreate,
) -> TagsModel:
    try:
        return await crud.create_entity(
            alchemy_model=TagsModel,
            pydantic_schema=tag,
            session=session,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete("/delete/{tag_id}", response_model=tags_schemas.TagDelete)
async def tags_delete_by_id(
    session: async_session_dependency,
    tag_id: UUID,
) -> TagsModel:
    deleted = await crud.delete_entity_by_field(
        alchemy_model=TagsModel,
        field_name="tag_id",
        field_value=tag_id,
        session=session,
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
