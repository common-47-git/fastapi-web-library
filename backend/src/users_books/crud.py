
from fastapi import HTTPException
from sqlalchemy import insert, select

from src.books.models import BooksModel
from src.database import async_session_dependency
from src.users.models.users import UsersModel
from src.users.models.users_books import UsersBooksModel


async def get_user_books(session: async_session_dependency, username: str):
    query = (
        select(BooksModel)
        .join(UsersBooksModel)
        .join(UsersModel)
        .filter(UsersModel.username == username)
    )
    result = await session.execute(query)
    books = result.scalars().all()
    return books


async def get_user_book_shelf(
    session: async_session_dependency, username: str, book_name: str,
):
    query = select(BooksModel.book_id).where(BooksModel.book_name == book_name)
    book_id = await session.execute(query)
    book_id = book_id.scalars().first()

    query = select(UsersModel.user_id).where(UsersModel.username == username)
    user_id = await session.execute(query)
    user_id = user_id.scalars().first()

    if not book_id:
        raise HTTPException(status_code=404, detail="Book not found.")

    query = (
        select(UsersBooksModel.book_shelf)
        .join(UsersModel, UsersBooksModel.user_id == UsersModel.user_id)
        .where(
            UsersBooksModel.book_id == book_id, UsersModel.user_id == user_id,
        )
    )
    result = await session.execute(query)
    shelf = result.scalars().first()

    return shelf if shelf else None


async def post_book_to_current_users_library(
    session: async_session_dependency,
    book_name: str,
    username: str,
    shelf_to_put: str,
):
    # Fetch the book ID
    stmt = select(BooksModel.book_id).where(BooksModel.book_name == book_name)
    result = await session.execute(stmt)
    book_id = result.scalars().first()

    if not book_id:
        raise HTTPException(
            status_code=404, detail=f"Book '{book_name}' not found",
        )

    # Fetch the user ID
    stmt = select(UsersModel.user_id).where(UsersModel.username == username)
    result = await session.execute(stmt)
    user_id = result.scalars().first()

    if not user_id:
        raise HTTPException(
            status_code=404, detail=f"User '{username}' not found",
        )

    # Insert into the users_books table
    stmt = insert(UsersBooksModel).values(
        user_id=user_id, book_id=book_id, book_shelf=shelf_to_put,
    )
    await session.execute(stmt)
    await session.commit()

    return {"user_id": user_id, "book_id": book_id, "book_shelf": shelf_to_put}
