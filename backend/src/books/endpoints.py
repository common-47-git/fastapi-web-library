import uuid
from collections.abc import Sequence

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import crud, http_exceptions
from backend.src.authors import crud as authors_crud
from backend.src.books import crud as books_crud
from backend.src.books import schemas as books_schemas
from backend.src.books.models import BooksModel
from backend.src.database import async_session_dependency
from backend.src.enums import ModulesEnum
from backend.src.tags import crud as tags_crud

router = APIRouter(
    prefix=f"/{ModulesEnum.BOOKS.value}",
    tags=[ModulesEnum.BOOKS],
)


@router.get(
    "/all",
    response_model=list[books_schemas.BookRead],
    summary="Get a list of books.",
)
async def books_all(
    session: async_session_dependency,
) -> Sequence[BooksModel]:
    """Get a list of books with full info: id, name etc."""
    books = await crud.read_entities(alchemy_model=BooksModel, session=session)
    if not books:
        raise http_exceptions.NotFound404
    return books


@router.get(
    "/{book_id}",
    response_model=books_schemas.BookFullInfo,
    summary="Get the book by id.",
)
async def books_get_by_id(
    book_id: uuid.UUID,
    session: async_session_dependency,
):
    """Get full book info by id, including authors, tags and the shelf."""
    book = await crud.read_entity_by_field(
        alchemy_model=BooksModel,
        field_name="book_id",
        field_value=book_id,
        session=session,
    )
    if not book:
        raise http_exceptions.NotFound404

    book_tags = await tags_crud.read_tags_by_book_id(
        book_id=book_id,
        session=session,
    )
    book_authors = await authors_crud.read_authors_by_book_id(
        book_id=book_id,
        session=session,
    )
    book_shelf = None

    return {
        "book_name": book.book_name,
        "book_country": book.book_country,
        "book_release_date": book.book_release_date,
        "book_translation_status": book.book_translation_status,
        "book_description": book.book_description,
        "book_cover": book.book_cover,
        "book_id": book.book_id,
        "book_tags": book_tags,
        "book_authors": book_authors,
        "book_shelf": book_shelf,
    }


@router.get(
    "/with-author/{author_id}",
    response_model=books_schemas.BookRead,
    summary="Get book by author.",
)
async def get_books_with_author_id(
    author_id: uuid.UUID,
    session: async_session_dependency,
) -> Sequence[BooksModel]:
    """Get book by it's author id if one exists."""
    books = await books_crud.read_books_by_author_id(
        author_id=author_id,
        session=session,
    )
    if not books:
        raise http_exceptions.NotFound404
    return books


@router.post(
    "/add",
    response_model=books_schemas.BookRead,
    status_code=status.HTTP_201_CREATED,
)
async def books_add(
    session: async_session_dependency,
    book: books_schemas.BookCreate,
) -> BooksModel:
    try:
        return await crud.create_entity(
            alchemy_model=BooksModel,
            pydantic_schema=book,
            session=session,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete("/delete/{book_id}", response_model=books_schemas.BookRead)
async def books_delete_by_id(
    book_id: uuid.UUID,
    session: async_session_dependency,
) -> BooksModel:
    deleted = await crud.delete_entity_by_field(
        alchemy_model=BooksModel,
        field_name="book_id",
        field_value=book_id,
        session=session,
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
