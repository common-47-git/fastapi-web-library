from typing import Annotated

from fastapi import APIRouter, Depends

from backend.src.books import schemas as books_schemas
from backend.src.database import async_session_dependency
from backend.src.users.crud import (
    get_user_books,
    post_book_to_current_users_library,
    read_current_user,
)
from backend.src.users.schemas import users as users_schemas

router = APIRouter(prefix="/users_books", tags=["users_books"])


@router.get("/books", response_model=list[books_schemas.BookRead])
async def read_user_books(
    current_user: Annotated[
        users_schemas.UserRead,
        Depends(read_current_user),
    ],
    session: async_session_dependency,
):
    return await get_user_books(
        username=current_user.username,
        session=session,
    )


@router.post("/bookmark")
async def add_book_to_current_users_library(
    book_name: str,
    shelf: str,
    current_user: Annotated[
        users_schemas.UserRead,
        Depends(read_current_user),
    ],
    session: async_session_dependency,
):
    book = await post_book_to_current_users_library(
        book_name=book_name,
        username=current_user.username,
        shelf_to_put=shelf,
        session=session,
    )
    return {"status": 200, "detail": "Book added to library", "data": book}
