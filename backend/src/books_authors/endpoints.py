from collections.abc import Sequence

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import crud, http_exceptions
from backend.src.books_authors import crud as books_authors_crud
from backend.src.books_authors import schemas as books_authors_schemas
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.database import async_session_dependency
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.BOOKS_AUTHORS.value}",
    tags=[ModulesEnum.BOOKS_AUTHORS],
)


@router.get(
    "/all",
    response_model=list[books_authors_schemas.BooksAuthorsRead],
)
async def books_authors_all(
    session: async_session_dependency,
) -> Sequence[BooksAuthorsModel]:
    books_authors_model = await crud.read_entities(
        alchemy_model=BooksAuthorsModel,
        session=session,
    )
    if not books_authors_model:
        raise http_exceptions.NotFound404
    return books_authors_model


@router.post(
    "/add",
    response_model=books_authors_schemas.BooksAuthorsCreate,
    status_code=status.HTTP_201_CREATED,
)
async def books_authors_add(
    session: async_session_dependency,
    books_authors: books_authors_schemas.BooksAuthorsCreate,
) -> BooksAuthorsModel:
    try:
        return await crud.create_entity(
            alchemy_model=BooksAuthorsModel,
            pydantic_schema=books_authors,
            session=session,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete(
    "/delete",
    response_model=books_authors_schemas.BooksAuthorsDelete,
)
async def books_authors_delete(
    books_authors: books_authors_schemas.BooksAuthorsDelete,
    session: async_session_dependency,
) -> BooksAuthorsModel:
    deleted = await books_authors_crud.delete_books_authors_entry_by_id(
        books_authors=books_authors,
        session=session,
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
