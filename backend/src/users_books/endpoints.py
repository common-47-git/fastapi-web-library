from typing import Annotated

from fastapi import APIRouter, Query, status

from backend.src.enums import ModulesEnum
from backend.src.users_books import schemas as users_books_schemas
from backend.src.users_books.services import UsersBooksServices

router = APIRouter(
    prefix=f"/{ModulesEnum.USERS_BOOKS.value}",
    tags=[ModulesEnum.USERS_BOOKS],
)


@router.get(
    "/",
    response_model=list[users_books_schemas.UsersBooksRead],
    summary="Get a list of books and books.",
)
async def books_books_all():
    """Get a list of entries book_id-book_id."""
    return await UsersBooksServices().read_all()


@router.post(
    "/add",
    response_model=users_books_schemas.UsersBooksRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book-book entry.",
)
async def books_books_add(
    books_books: users_books_schemas.UsersBooksRead,
):
    """Create an entry book_id-book_id."""
    return await UsersBooksServices().create_one(
        pydantic_schema=books_books,
    )


@router.delete(
    "/delete",
    response_model=users_books_schemas.UsersBooksRead,
    summary="Delete a book-book entry.",
)
async def books_books_delete(
    user_book: Annotated[users_books_schemas.UsersBooksDelete, Query()],
):
    return await UsersBooksServices().delete_users_books_by_id(
        users_books=user_book,
    )
