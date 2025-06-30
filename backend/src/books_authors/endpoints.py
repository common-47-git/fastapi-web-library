import uuid
from collections.abc import Sequence

from fastapi import APIRouter, status

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
async def books_authors_all() -> Sequence[BooksAuthorsModel]:
    """Get a list of entries book_id-author_id."""
    return await BooksAuthorsServices().read_all()


@router.post(
    "/add",
    response_model=books_authors_schemas.BooksAuthorsCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book-author entry.",
)
async def books_authors_add(
    books_authors: books_authors_schemas.BooksAuthorsCreate,
) -> BooksAuthorsModel:
    """Create an entry book_id-author_id."""
    return await BooksAuthorsServices().create_one(
        pydantic_schema=books_authors,
    )


@router.delete(
    "/delete",
    response_model=books_authors_schemas.BooksAuthorsDelete,
    summary="Delete a book-author entry.",
)
async def books_authors_delete(
    book_id: uuid.UUID,
    author_id: uuid.UUID,
) -> BooksAuthorsModel | None:
    """Delete an entry book_id-author_id."""
    books_authors = books_authors_schemas.BooksAuthorsDelete(
        book_id=book_id,
        author_id=author_id,
    )
    return await BooksAuthorsServices().delete_books_authors_entry_by_id(
        books_authors=books_authors,
    )
