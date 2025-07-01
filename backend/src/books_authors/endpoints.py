from typing import Annotated

from fastapi import APIRouter, Query, status

from backend.src.books_authors import schemas as books_authors_schemas
from backend.src.books_authors.models import BooksAuthorsModel
from backend.src.books_authors.services import BooksAuthorsServices
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
async def books_authors_all():
    """Get a list of entries book_id-author_id."""
    return await BooksAuthorsServices().read_all()


@router.post(
    "/add",
    response_model=books_authors_schemas.BooksAuthorsCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book-author entry.",
)
async def books_authors_add(
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
)
async def books_authors_delete(
    book_author: Annotated[books_authors_schemas.BooksAuthorsDelete, Query()],
) -> BooksAuthorsModel | None:
    """Delete an entry book_id-author_id or raise 404."""
    return await BooksAuthorsServices().delete_books_authors_entry_by_id(
        book_author=book_author,
    )
