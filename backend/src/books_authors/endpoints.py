from typing import Annotated

from fastapi import APIRouter, Query, status

from backend.src import http_exceptions
from backend.src.books_authors import schemas as books_authors_schemas
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.books_authors.services import BooksAuthorsServices
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.BOOKS_AUTHORS.value}",
    tags=[ModulesEnum.BOOKS_AUTHORS],
)


@router.get(
    "/",
    response_model=list[books_authors_schemas.BooksAuthorsRead],
    summary="Get a list of books and authors.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_all_books_authors():
    """Get a list of entries book_id-author_id."""
    return await BooksAuthorsServices().read_all()


@router.post(
    "/add",
    response_model=books_authors_schemas.BooksAuthorsCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book-author entry.",
    responses={
        201: http_exceptions.Created201().get_response_body(),
        409: http_exceptions.Conflict409().get_response_body(),
    },
)
async def post_book_author(
    book_author: books_authors_schemas.BooksAuthorsCreate,
):
    """Create an entry book_id-author_id."""
    return await BooksAuthorsServices().create_one(
        pydantic_schema=book_author,
    )


@router.delete(
    "/delete",
    response_model=books_authors_schemas.BooksAuthorsDelete,
    summary="Delete a book-author entry.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def delete_book_author(
    book_author: Annotated[books_authors_schemas.BooksAuthorsDelete, Query()],
) -> BooksAuthorsModel | None:
    """Delete an entry book_id-author_id or raise 404."""
    return await BooksAuthorsServices().delete_books_authors_entry_by_id(
        book_author=book_author,
    )
