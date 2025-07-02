from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from backend.src.books.schemas import BookCreate, BookInDB
from backend.src.volumes.schemas import VolumeCreate


async def test_post_volume(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
):
    book_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_response.status_code == status.HTTP_201_CREATED
    book_id = book_response.json()["book_id"]

    volume_data = VolumeCreate(
        book_id=book_id,
        volume_number=1,
        volume_name="Test Volume",
    )
    volume_response = await async_client.post(
        "/volumes/add",
        json=jsonable_encoder(volume_data),
    )
    assert volume_response.status_code == status.HTTP_201_CREATED


async def test_post_volume_conflict(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
):
    book_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_response.status_code == status.HTTP_201_CREATED
    book_id = book_response.json()["book_id"]

    volume_data = VolumeCreate(
        book_id=book_id,
        volume_number=1,
        volume_name="Conflict Volume",
    )
    response1 = await async_client.post(
        "/volumes/add",
        json=jsonable_encoder(volume_data),
    )
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = await async_client.post(
        "/volumes/add",
        json=jsonable_encoder(volume_data),
    )
    assert response2.status_code == status.HTTP_409_CONFLICT


async def test_delete_volume_not_found(async_client: AsyncClient):
    import uuid

    fake_volume_id = uuid.uuid4()
    response = await async_client.delete(f"/volumes/{fake_volume_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
