from typing import Annotated

from fastapi import APIRouter, Query, status

from backend.src import http_exceptions
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
    summary="Get a list of books and users.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_users_books_all():
    """Get a list of entries book_id-book_id."""
    return await UsersBooksServices().read_all()


@router.post(
    "/add",
    response_model=users_books_schemas.UsersBooksRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book-user entry.",
    responses={
        201: http_exceptions.OK200().get_response_body(),
        409: http_exceptions.Conflict409().get_response_body(),
    },
)
async def post_user_book(
    books_books: users_books_schemas.UsersBooksCreate,
):
    """Create an entry book_id-user_id."""
    return await UsersBooksServices().create_one(
        pydantic_schema=books_books,
    )


@router.get(
    "/with-ids/",
    response_model=users_books_schemas.UsersBooksRead,
    summary="Get the book-user entry by id.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_user_book_by_id(
    user_book: Annotated[users_books_schemas.UsersBooksBase, Query()],
):
    """Get the book-user entry and book shelf by id."""
    return await UsersBooksServices().read_user_book_by_id(user_book=user_book)


@router.patch(
    "/update",
    response_model=users_books_schemas.UsersBooksRead,
    summary="Update a book-user entry.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def update_user_book_shelf(
    user_book: users_books_schemas.UsersBooksUpdate,
):
    """Update book shelf by book_id-user_id."""
    return await UsersBooksServices().update_shelf_by_id(
        user_book=user_book,
    )


@router.delete(
    "/delete",
    response_model=users_books_schemas.UsersBooksRead,
    summary="Delete a book-user entry.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def delete_user_book(
    user_book: Annotated[users_books_schemas.UsersBooksDelete, Query()],
):
    """Delete an entry user_id-book_id or raise 404."""
    return await UsersBooksServices().delete_users_books_by_id(
        users_books=user_book,
    )
