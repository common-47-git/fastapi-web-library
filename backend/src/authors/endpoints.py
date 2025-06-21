from uuid import UUID

from fastapi import APIRouter, status

from backend.src import crud, status_codes
from backend.src.authors import schemas as authors_schemas
from backend.src.authors.models import AuthorsModel
from backend.src.database import async_session_dependency
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.AUTHORS.value}",
    tags=[ModulesEnum.AUTHORS],
)


@router.get("/all", response_model=list[authors_schemas.AuthorRead])
async def authors_all(session: async_session_dependency):
    authors = await crud.read_entities(
        alchemy_model=AuthorsModel,
        session=session,
    )
    if not authors:
        raise status_codes.NotFound_404()
    return authors


@router.post(
    "/add",
    response_model=authors_schemas.AuthorCreate,
    status_code=status.HTTP_201_CREATED,
)
async def authors_add(
    author: authors_schemas.AuthorCreate,
    session: async_session_dependency,
):
    return await crud.create_entity(
        alchemy_model=AuthorsModel,
        pydantic_schema=author,
        session=session,
    )


@router.delete(
    "/delete/{author_id}",
    response_model=authors_schemas.AuthorDelete,
)
async def authors_delete_by_id(
    author_id: UUID,
    session: async_session_dependency,
):
    return await crud.delete_entity_by_field(
        alchemy_model=AuthorsModel,
        field_name="author_id",
        field_value=author_id,
        session=session,
    )
