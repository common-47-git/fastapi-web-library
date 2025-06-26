from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.authors import schemas as authors_schemas
from backend.src.authors.models import AuthorsModel
from backend.src.authors.repository import AuthorsRepository
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.AUTHORS.value}",
    tags=[ModulesEnum.AUTHORS],
)


@router.get(
    "/",
    response_model=list[authors_schemas.AuthorRead],
    summary="Get a list of authors.",
)
async def authors_all() -> Sequence[AuthorsModel] | None:
    """Get a list of authors with full info: id, name etc."""
    authors = await AuthorsRepository().read_all()
    if not authors:
        raise http_exceptions.NotFound404
    return authors


@router.post(
    "/add",
    response_model=authors_schemas.AuthorRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an author.",
)
async def authors_add(
    author: authors_schemas.AuthorCreate,
):
    """Create an author with properties specified in given schema."""
    try:
        return await AuthorsRepository().create_one(
            pydantic_schema=author,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete(
    "/{author_id}",
    response_model=authors_schemas.AuthorDelete,
    summary="Delete an author.",
)
async def authors_delete_by_id(
    author_id: UUID,
) -> AuthorsModel | None:
    """Delete an author by id."""
    deleted = await AuthorsRepository().delete_one_by_property(
        property_name=AuthorsModel.author_id.key,
        property_value=author_id,
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
