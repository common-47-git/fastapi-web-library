from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import crud, status_codes
from backend.src.books_authors import crud as books_authors_crud
from backend.src.books_authors import schemas as books_authors_schemas
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.database import async_session_dependency

router = APIRouter(prefix="/books_authors", tags=["books_authors"])


@router.get(
    "/all", response_model=list[books_authors_schemas.BooksAuthorsRead],
)
async def books_authors_all(
    session: async_session_dependency,
):
    books_authors_model = await crud.read_entities(
        alchemy_model=BooksAuthorsModel, session=session,
    )
    if not books_authors_model:
        raise status_codes.NotFound_404()
    return books_authors_model


@router.post(
    "/add",
    response_model=books_authors_schemas.BooksAuthorsCreate,
    status_code=status.HTTP_201_CREATED,
)
async def books_authors_add(
    session: async_session_dependency,
    books_authors: books_authors_schemas.BooksAuthorsCreate,
):
    try:
        entity = await crud.create_entity(
            alchemy_model=BooksAuthorsModel,
            pydantic_schema=books_authors,
            session=session,
        )
        return entity
    except IntegrityError as e:
        raise status_codes.Conflict_409(exception=e)


@router.delete("/delete")
async def books_authors_delete(
    books_authors: books_authors_schemas.BooksAuthorsDelete,
    session: async_session_dependency,
):
    deleted = await books_authors_crud.delete_books_authors_by_id(
        books_authors=books_authors, session=session,
    )
    if not deleted:
        raise status_codes.NotFound_404()
    return deleted
