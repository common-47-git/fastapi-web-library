from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from backend.src.books.schemas import BookCreate, BookInDB


async def test_get_all_books(async_client: AsyncClient):
    response = await async_client.get("/books/")
    assert response.status_code in (
        status.HTTP_200_OK,
        status.HTTP_404_NOT_FOUND,
    )


async def test_post_book(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
):
    response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )

    assert response.status_code == status.HTTP_201_CREATED

    book_id = response.json()["book_id"]

    delete_response = await async_client.delete(f"/books/{book_id}")
    assert delete_response.status_code == status.HTTP_200_OK


async def test_post_book_conflict(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
):
    response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )

    assert response.status_code == status.HTTP_201_CREATED

    book_id = response.json()["book_id"]

    response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )

    assert response.status_code == status.HTTP_409_CONFLICT

    delete_response = await async_client.delete(f"/books/{book_id}")
    assert delete_response.status_code == status.HTTP_200_OK


async def test_delete_book(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
):
    create_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )

    assert create_response.status_code == status.HTTP_201_CREATED
    book_id = create_response.json()["book_id"]

    delete_response = await async_client.delete(f"/books/{book_id}")
    assert delete_response.status_code == status.HTTP_200_OK

    get_response = await async_client.get(f"/books/{book_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_book_not_found(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
):
    delete_response = await async_client.delete(
        f"/books/{test_book_in_db.book_id}",
    )
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
