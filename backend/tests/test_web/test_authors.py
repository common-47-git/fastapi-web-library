from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from backend.src.authors.schemas import AuthorCreate, AuthorInDB


async def test_get_all_authors(async_client: AsyncClient):
    response = await async_client.get("/authors/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_post_author(
    async_client: AsyncClient,
    test_author_in_db: AuthorInDB,
):
    response = await async_client.post(
        "/authors/add",
        json=jsonable_encoder(AuthorCreate(**test_author_in_db.model_dump())),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["author_name"] == test_author_in_db.author_name


async def test_post_author_conflict(
    async_client: AsyncClient,
    test_author_in_db: AuthorInDB,
):
    response = await async_client.post(
        "/authors/add",
        json=jsonable_encoder(AuthorCreate(**test_author_in_db.model_dump())),
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = await async_client.post(
        "/authors/add",
        json=jsonable_encoder(AuthorCreate(**test_author_in_db.model_dump())),
    )

    assert response.status_code == status.HTTP_409_CONFLICT


async def test_delete_author(
    async_client: AsyncClient,
    test_author_in_db: AuthorInDB,
):
    create_response = await async_client.post(
        "/authors/add",
        json=jsonable_encoder(AuthorCreate(**test_author_in_db.model_dump())),
    )

    assert create_response.status_code == status.HTTP_201_CREATED
    author_id = create_response.json()["author_id"]

    delete_response = await async_client.delete(f"/authors/{author_id}")
    assert delete_response.status_code == status.HTTP_200_OK

    get_response = await async_client.get(f"/authors/{author_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_author_not_found(
    async_client: AsyncClient,
    test_author_in_db: AuthorInDB,
):
    delete_response = await async_client.delete(
        f"/authors/{test_author_in_db.author_id}",
    )
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
