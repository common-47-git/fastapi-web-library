from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from backend.src.books.schemas import BookCreate, BookInDB
from backend.src.chapters.schemas import ChapterCreate
from backend.src.volumes.schemas import VolumeCreate


async def test_post_chapter(
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
    volume_id = volume_response.json()["volume_id"]

    chapter_data = ChapterCreate(
        volume_id=volume_id,
        chapter_number=1,
        chapter_name="Test Chapter",
        chapter_content="This is the text of the chapter.",
    )
    chapter_response = await async_client.post(
        "/chapters/add",
        json=jsonable_encoder(chapter_data),
    )
    assert chapter_response.status_code == status.HTTP_201_CREATED
    chapter_id = chapter_response.json()["chapter_id"]

    delete_chapter_response = await async_client.delete(
        f"/chapters/{chapter_id}",
    )
    assert delete_chapter_response.status_code == status.HTTP_200_OK

    delete_volume_response = await async_client.delete(f"/volumes/{volume_id}")
    assert delete_volume_response.status_code == status.HTTP_200_OK

    delete_book_response = await async_client.delete(f"/books/{book_id}")
    assert delete_book_response.status_code == status.HTTP_200_OK


async def test_post_chapter_conflict(
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
    volume_id = volume_response.json()["volume_id"]

    chapter_data = ChapterCreate(
        volume_id=volume_id,
        chapter_number=1,
        chapter_name="Test Chapter",
        chapter_content="This is the text of the chapter.",
    )
    chapter_response = await async_client.post(
        "/chapters/add",
        json=jsonable_encoder(chapter_data),
    )
    assert chapter_response.status_code == status.HTTP_201_CREATED

    conflict_response = await async_client.post(
        "/chapters/add",
        json=jsonable_encoder(chapter_data),
    )
    assert conflict_response.status_code == status.HTTP_409_CONFLICT


async def test_read_chapter_by_book_name(
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
        volume_name="Volume 1",
    )
    volume_response = await async_client.post(
        "/volumes/add",
        json=jsonable_encoder(volume_data),
    )
    assert volume_response.status_code == status.HTTP_201_CREATED
    volume_id = volume_response.json()["volume_id"]

    chapter_data = ChapterCreate(
        volume_id=volume_id,
        chapter_number=1,
        chapter_name="Intro",
        chapter_content="Start of the book.",
    )
    chapter_response = await async_client.post(
        "/chapters/add",
        json=jsonable_encoder(chapter_data),
    )
    assert chapter_response.status_code == status.HTTP_201_CREATED

    read_response = await async_client.get(
        f"/chapters/read/{test_book_in_db.book_name}",
    )
    assert read_response.status_code == status.HTTP_200_OK
