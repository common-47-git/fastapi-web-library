from backend.src import http_exceptions
from backend.src.services import BaseServices
from backend.src.users_books import schemas as users_books_schemas
from backend.src.users_books.models import UsersBooksModel
from backend.src.users_books.repository import UsersBooksRepository


class UsersBooksServices(BaseServices):
    alchemy_model: type[UsersBooksModel] = UsersBooksModel
    repository: type[UsersBooksRepository] = UsersBooksRepository

    async def read_user_book_by_id(
        self,
        user_book: users_books_schemas.UsersBooksBase,
    ):
        entry = await UsersBooksRepository().read_user_book_by_ids(
            user_id=user_book.user_id,
            book_id=user_book.book_id,
        )
        if not entry:
            raise http_exceptions.NotFound404
        return entry

    async def update_shelf_by_id(
        self,
        user_book: users_books_schemas.UsersBooksUpdate,
    ):
        entry = await UsersBooksRepository().update_shelf_by_ids(
            user_id=user_book.user_id,
            book_id=user_book.book_id,
            book_shelf=user_book.book_shelf,
        )
        if not entry:
            raise http_exceptions.NotFound404
        return entry

    async def delete_users_books_by_id(
        self,
        users_books: users_books_schemas.UsersBooksDelete,
    ):
        deleted = await UsersBooksRepository().delete_users_books_by_ids(
            user_id=users_books.user_id,
            book_id=users_books.book_id,
        )
        if not deleted:
            raise http_exceptions.NotFound404
        return deleted
