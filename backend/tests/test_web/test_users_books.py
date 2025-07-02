from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from backend.src.books.schemas import BookCreate, BookInDB
from backend.src.users.schemas.users import UserCreate, UserInDB
from backend.src.users_books.schemas import (
    UsersBooksDelete,
    UsersBooksRead,
)


async def test_get_all_users_books(async_client: AsyncClient):
    response = await async_client.get("/users_books/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_post_users_books(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_user_in_db: UserInDB,
):
    # create book
    book_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_response.status_code == status.HTTP_201_CREATED
    book_id = book_response.json()["book_id"]

    # create user
    user_response = await async_client.post(
        "/users/add",
        json=jsonable_encoder(UserCreate(**test_user_in_db.model_dump())),
    )
    assert user_response.status_code == status.HTTP_201_CREATED
    user_id = user_response.json()["user_id"]

    # create relation
    relation = UsersBooksRead(book_id=book_id, user_id=user_id)
    relation_response = await async_client.post(
        "/users_books/add",
        json=jsonable_encoder(relation),
    )
    assert relation_response.status_code == status.HTTP_201_CREATED


async def test_post_users_books_conflict(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_user_in_db: UserInDB,
):
    book_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_response.status_code == status.HTTP_201_CREATED
    book_id = book_response.json()["book_id"]

    user_response = await async_client.post(
        "/users/add",
        json=jsonable_encoder(UserCreate(**test_user_in_db.model_dump())),
    )
    assert user_response.status_code == status.HTTP_201_CREATED
    user_id = user_response.json()["user_id"]

    relation = UsersBooksRead(book_id=book_id, user_id=user_id)
    await async_client.post(
        "/users_books/add",
        json=jsonable_encoder(relation),
    )

    conflict_response = await async_client.post(
        "/users_books/add",
        json=jsonable_encoder(relation),
    )
    assert conflict_response.status_code == status.HTTP_409_CONFLICT


async def test_delete_users_books(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_user_in_db: UserInDB,
):
    book_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_response.status_code == status.HTTP_201_CREATED
    book_id = book_response.json()["book_id"]

    user_response = await async_client.post(
        "/users/add",
        json=jsonable_encoder(UserCreate(**test_user_in_db.model_dump())),
    )
    assert user_response.status_code == status.HTTP_201_CREATED
    user_id = user_response.json()["user_id"]

    relation = UsersBooksRead(book_id=book_id, user_id=user_id)
    await async_client.post(
        "/users_books/add",
        json=jsonable_encoder(relation),
    )

    delete_response = await async_client.delete(
        f"/users_books/delete?book_id={book_id}&user_id={user_id}",
    )
    assert delete_response.status_code == status.HTTP_200_OK

    await async_client.delete(f"/books/{book_id}")
    await async_client.delete(f"/users/{user_id}")


async def test_delete_users_books_not_found(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_user_in_db: UserInDB,
):
    relation = UsersBooksDelete(
        book_id=test_book_in_db.book_id,
        user_id=test_user_in_db.user_id,
    )
    response = await async_client.delete(
        f"/users_books/delete?book_id={relation.book_id}&user_id={relation.user_id}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
