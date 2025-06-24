import uuid
from collections.abc import Sequence

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.authors.repository import AuthorsRepository
from backend.src.books import schemas as books_schemas
from backend.src.tags import schemas as tags_schemas
from backend.src.books.models import BooksModel
from backend.src.books.repository import BooksRepository
from backend.src.enums import ModulesEnum
from backend.src.tags.repository import TagsRepository

router = APIRouter(
    prefix=f"/{ModulesEnum.BOOKS.value}",
    tags=[ModulesEnum.BOOKS],
)


@router.get(
    "/all",
    response_model=list[books_schemas.BookRead],
    summary="Get a list of books.",
)
async def books_all() -> Sequence[BooksModel]:
    """Get a list of books with full info: id, name etc."""
    books = await BooksRepository().read_all()
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
):
    """Get full book info by id, including authors, tags and the shelf."""
    book = await BooksRepository().read_one_by_property(
        property_name=BooksModel.book_id.key,
        property_value=book_id,
    )
    if not book:
        raise http_exceptions.NotFound404

    tags = await TagsRepository().read_tags_by_book_id(
        book_id=book_id,
    )
    book_tags = [tags_schemas.TagRead.model_validate(tag, from_attributes=True) for tag in tags]
    book_authors = await AuthorsRepository().read_authors_by_book_id(
        book_id=book_id,
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
    response_model=list[books_schemas.BookRead],
    summary="Get books by author.",
)
async def get_books_with_author_id(
    author_id: uuid.UUID,
) -> Sequence[BooksModel]:
    """Get books by it's author id, if one exists."""
    books = await BooksRepository().read_books_by_author_id(
        author_id=author_id,
    )
    if not books:
        raise http_exceptions.NotFound404
    return books


@router.post(
    "/add",
    response_model=books_schemas.BookRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book.",
)
async def books_add(
    book: books_schemas.BookCreate,
):
    """Create a book with properties specified in given schema."""
    try:
        return await BooksRepository().create_one(
            pydantic_schema=book,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete(
    "/{book_id}",
    response_model=books_schemas.BookDelete,
    summary="Delete a book.",
)
async def books_delete_by_id(
    book_id: uuid.UUID,
) -> BooksModel:
    """Delete a book by id."""
    deleted = await BooksRepository().delete_one_by_property(
        property_name=BooksModel.book_id.key,
        property_value=book_id,
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
