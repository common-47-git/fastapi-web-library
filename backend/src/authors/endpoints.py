from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.src.authors import schemas as authors_schemas
from backend.src.authors.deps import AuthorsDeps
from backend.src.authors.models import AuthorsModel
from backend.src.authors.services import AuthorsServices
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
async def authors_all():
    """Get a list of authors with full info: id, name etc or raise 404."""
    return await AuthorsServices().read_all()


@router.post(
    "/add",
    response_model=authors_schemas.AuthorRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an author.",
)
async def authors_add(
    author: authors_schemas.AuthorCreate,
):
    """Create an author with properties specified in given schema or raise 409."""
    return await AuthorsServices().create_one(
        pydantic_schema=author,
    )


@router.delete(
    "/{author_id}",
    response_model=authors_schemas.AuthorRead,
    summary="Delete an author.",
)
async def authors_delete_by_id(
    existing_author: Annotated[AuthorsModel, Depends(AuthorsDeps.one_exists)],
):
    """Delete an author by id or raise 404."""
    return await AuthorsServices().delete_one(alchemy_object=existing_author)
