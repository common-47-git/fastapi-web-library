import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.src import http_exceptions
from backend.src.books import schemas as books_schemas
from backend.src.books.deps import BooksDeps
from backend.src.books.models import BooksModel
from backend.src.books.services import BooksServices
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.BOOKS.value}",
    tags=[ModulesEnum.BOOKS],
)


@router.get(
    "/",
    response_model=list[books_schemas.BookRead],
    summary="Get a list of books.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def books_all() -> list[books_schemas.BookRead]:
    """Get a list of books with full info: id, name etc or raise 404."""
    return await BooksServices().read_all()


@router.get(
    "/{book_id}",
    response_model=books_schemas.BookFullInfo,
    summary="Get the book by id.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def books_get_by_id(
    book_id: uuid.UUID,
):
    """Get full book info by id, including authors, tags and the shelf."""
    return await BooksServices().read_full_book_info_by_id(book_id=book_id)


@router.get(
    "/with-author/{author_id}",
    response_model=list[books_schemas.BookRead],
    summary="Get books by author.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_books_with_author_id(
    author_id: uuid.UUID,
) -> list[books_schemas.BookRead]:
    """Get books by it's author id, or raise 404."""
    return await BooksServices().read_books_by_author_id(
        author_id=author_id,
    )


@router.post(
    "/add",
    response_model=books_schemas.BookRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book.",
    responses={
        201: http_exceptions.Created201().get_response_body(),
        409: http_exceptions.Conflict409().get_response_body(),
    },
)
async def books_add(
    book: books_schemas.BookCreate,
):
    """Create a book with properties specified in given schema or raise 409."""
    return await BooksServices().create_one(
        pydantic_schema=book,
    )


@router.delete(
    "/{book_id}",
    response_model=books_schemas.BookDelete,
    summary="Delete a book.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def books_delete_by_id(
    existing_book: Annotated[BooksModel, Depends(BooksDeps.one_exists)],
):
    """Delete a book by id or raise 404."""
    return await BooksServices().delete_one(
        alchemy_object=existing_book,
    )
