from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import crud, http_exceptions
from backend.src.authors import schemas as authors_schemas
from backend.src.authors.models import AuthorsModel
from backend.src.database import async_session_dependency
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.AUTHORS.value}",
    tags=[ModulesEnum.AUTHORS],
)


@router.get(
    "/all",
    response_model=list[authors_schemas.AuthorRead],
    summary="Get a list of authors.",
)
async def authors_all(
    session: async_session_dependency,
) -> Sequence[AuthorsModel] | None:
    """Get a list of authors with full info: id, name etc."""
    authors = await crud.read_entities(
        alchemy_model=AuthorsModel,
        session=session,
    )
    if not authors:
        raise http_exceptions.NotFound404
    return authors


@router.post(
    "/add",
    response_model=authors_schemas.AuthorCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Create an author.",
)
async def authors_add(
    author: authors_schemas.AuthorCreate,
    session: async_session_dependency,
) -> AuthorsModel:
    """Create an author with properties specified in given schema."""
    try:
        return await crud.create_entity(
            alchemy_model=AuthorsModel,
            pydantic_schema=author,
            session=session,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete(
    "/delete/{author_id}",
    response_model=authors_schemas.AuthorDelete,
    summary="Delete an author.",
)
async def authors_delete_by_id(
    author_id: UUID,
    session: async_session_dependency,
) -> AuthorsModel | None:
    """Delete an author by id."""
    deleted = await crud.delete_entity_by_field(
        alchemy_model=AuthorsModel,
        field_name=AuthorsModel.author_id.key,
        field_value=author_id,
        session=session,
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
