import uuid

from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from backend.src.books.schemas import BookCreate, BookInDB
from backend.src.books_tags.schemas import BooksTagsCreate
from backend.src.tags.schemas import TagCreate


async def test_get_all_not_found(async_client: AsyncClient):
    response = await async_client.get("/books_tags/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_post_books_tags(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_tag_in_db: TagCreate,
):
    # Create book
    book_resp = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_resp.status_code == status.HTTP_201_CREATED
    book_id = book_resp.json()["book_id"]

    # Create tag
    tag_resp = await async_client.post(
        "/tags/add",
        json=jsonable_encoder(test_tag_in_db),
    )
    assert tag_resp.status_code == status.HTTP_201_CREATED
    tag_id = tag_resp.json()["tag_id"]

    # Create book-tag relation
    relation = BooksTagsCreate(book_id=book_id, tag_id=tag_id)
    create_resp = await async_client.post(
        "/books_tags/add",
        json=jsonable_encoder(relation),
    )
    assert create_resp.status_code == status.HTTP_201_CREATED


async def test_post_books_tags_conflict(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_tag_in_db: TagCreate,
):
    # Create book
    book_resp = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_resp.status_code == status.HTTP_201_CREATED
    book_id = book_resp.json()["book_id"]

    # Create tag
    tag_resp = await async_client.post(
        "/tags/add",
        json=jsonable_encoder(test_tag_in_db),
    )
    assert tag_resp.status_code == status.HTTP_201_CREATED
    tag_id = tag_resp.json()["tag_id"]

    # First creation
    relation = BooksTagsCreate(book_id=book_id, tag_id=tag_id)
    resp1 = await async_client.post(
        "/books_tags/add",
        json=jsonable_encoder(relation),
    )
    assert resp1.status_code == status.HTTP_201_CREATED

    # Conflict creation
    resp2 = await async_client.post(
        "/books_tags/add",
        json=jsonable_encoder(relation),
    )
    assert resp2.status_code == status.HTTP_409_CONFLICT


async def test_delete_books_tags_not_found(
    async_client: AsyncClient,
):
    fake_book_id = uuid.uuid4()
    fake_tag_id = uuid.uuid4()
    response = await async_client.delete(
        f"/books_tags/delete?book_id={fake_book_id}&tag_id={fake_tag_id}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
