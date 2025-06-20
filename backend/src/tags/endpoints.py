from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from src import crud, status_codes
from src.database import async_session_dependency
from src.tags import schemas as tags_schemas
from src.tags.models import TagsModel

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/all", response_model=list[tags_schemas.TagRead])
async def tags_all(session: async_session_dependency):
    tags = await crud.read_entities(alchemy_model=TagsModel, session=session)
    if not tags:
        raise status_codes.NotFound_404()
    return tags


@router.post(
    "/add",
    response_model=tags_schemas.TagCreate,
    status_code=status.HTTP_201_CREATED,
)
async def tags_add(
    session: async_session_dependency,
    tag: tags_schemas.TagCreate,
):
    try:
        entity = await crud.create_entity(
            alchemy_model=TagsModel, pydantic_schema=tag, session=session,
        )
        return entity
    except IntegrityError as e:
        raise status_codes.Conflict_409(exception=e)


@router.delete("/delete/{tag_id}", response_model=tags_schemas.TagDelete)
async def tags_delete_by_id(
    session: async_session_dependency,
    tag_id: UUID,
):
    deleted = await crud.delete_entity_by_field(
        alchemy_model=TagsModel,
        field_name="tag_id",
        field_value=tag_id,
        session=session,
    )
    if not deleted:
        raise status_codes.NotFound_404()
    return deleted
