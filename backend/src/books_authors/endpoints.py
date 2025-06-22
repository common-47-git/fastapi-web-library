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
    summary="Get a list of books and authors.",
)
async def books_authors_all(
    session: async_session_dependency,
) -> Sequence[BooksAuthorsModel]:
    """Get a list of entries book_id-author_id."""
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
    summary="Create a book-author entry.",
)
async def books_authors_add(
    session: async_session_dependency,
    books_authors: books_authors_schemas.BooksAuthorsCreate,
) -> BooksAuthorsModel:
    """Create an entry book_id-author_id."""
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
    summary="Delete a book-author entry.",
)
async def books_authors_delete(
    books_authors: books_authors_schemas.BooksAuthorsDelete,
    session: async_session_dependency,
) -> BooksAuthorsModel:
    """Delete an entry book_id-author_id."""
    deleted = await books_authors_crud.delete_books_authors_entry_by_id(
        books_authors=books_authors,
        session=session,
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
