from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from backend.src.authors.schemas import AuthorCreate, AuthorInDB
from backend.src.books.schemas import BookCreate, BookInDB
from backend.src.books_authors.schemas import (
    BooksAuthorsCreate,
    BooksAuthorsDelete,
)


async def test_get_all_books_authors(async_client: AsyncClient):
    response = await async_client.get("/books_authors/all")
    assert response.status_code in (
        status.HTTP_200_OK,
        status.HTTP_404_NOT_FOUND,
    )


async def test_post_books_authors(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_author_in_db: AuthorInDB,
):
    # create book
    book_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_response.status_code == status.HTTP_201_CREATED
    book_id = book_response.json()["book_id"]

    # create author
    author_response = await async_client.post(
        "/authors/add",
        json=jsonable_encoder(AuthorCreate(**test_author_in_db.model_dump())),
    )
    assert author_response.status_code == status.HTTP_201_CREATED
    author_id = author_response.json()["author_id"]

    # create relation
    relation = BooksAuthorsCreate(book_id=book_id, author_id=author_id)
    relation_response = await async_client.post(
        "/books_authors/add",
        json=jsonable_encoder(relation),
    )
    assert relation_response.status_code == status.HTTP_201_CREATED

    # cleanup
    delete_relation_response = await async_client.delete(
        f"/books_authors/delete?book_id={relation.book_id}&author_id={relation.author_id}",
    )
    assert delete_relation_response.status_code == status.HTTP_200_OK

    delete_book_response = await async_client.delete(f"/books/{book_id}")
    assert delete_book_response.status_code == status.HTTP_200_OK

    delete_author_response = await async_client.delete(f"/authors/{author_id}")
    assert delete_author_response.status_code == status.HTTP_200_OK


async def test_post_books_authors_conflict(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_author_in_db: AuthorInDB,
):
    # create book
    book_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_response.status_code == status.HTTP_201_CREATED
    book_id = book_response.json()["book_id"]

    # create author
    author_response = await async_client.post(
        "/authors/add",
        json=jsonable_encoder(AuthorCreate(**test_author_in_db.model_dump())),
    )
    assert author_response.status_code == status.HTTP_201_CREATED
    author_id = author_response.json()["author_id"]

    # create relation
    relation = BooksAuthorsCreate(book_id=book_id, author_id=author_id)
    relation_response = await async_client.post(
        "/books_authors/add",
        json=jsonable_encoder(relation),
    )
    assert relation_response.status_code == status.HTTP_201_CREATED

    # second attempt = conflict
    relation_conflict = await async_client.post(
        "/books_authors/add",
        json=jsonable_encoder(relation),
    )
    assert relation_conflict.status_code == status.HTTP_409_CONFLICT

    # cleanup
    delete_relation_response = await async_client.delete(
        f"/books_authors/delete?book_id={relation.book_id}&author_id={relation.author_id}",
    )
    assert delete_relation_response.status_code == status.HTTP_200_OK

    delete_book_response = await async_client.delete(f"/books/{book_id}")
    assert delete_book_response.status_code == status.HTTP_200_OK

    delete_author_response = await async_client.delete(f"/authors/{author_id}")
    assert delete_author_response.status_code == status.HTTP_200_OK


async def test_delete_books_authors(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_author_in_db: AuthorInDB,
):
    book_response = await async_client.post(
        "/books/add",
        json=jsonable_encoder(BookCreate(**test_book_in_db.model_dump())),
    )
    assert book_response.status_code == status.HTTP_201_CREATED
    book_id = book_response.json()["book_id"]

    author_response = await async_client.post(
        "/authors/add",
        json=jsonable_encoder(AuthorCreate(**test_author_in_db.model_dump())),
    )
    assert author_response.status_code == status.HTTP_201_CREATED
    author_id = author_response.json()["author_id"]

    relation = BooksAuthorsCreate(book_id=book_id, author_id=author_id)
    relation_response = await async_client.post(
        "/books_authors/add",
        json=jsonable_encoder(relation),
    )
    assert relation_response.status_code == status.HTTP_201_CREATED

    delete_response = await async_client.delete(
        f"/books_authors/delete?book_id={book_id}&author_id={author_id}",
    )
    assert delete_response.status_code == status.HTTP_200_OK

    delete_book_response = await async_client.delete(f"/books/{book_id}")
    assert delete_book_response.status_code == status.HTTP_200_OK

    delete_author_response = await async_client.delete(f"/authors/{author_id}")
    assert delete_author_response.status_code == status.HTTP_200_OK


async def test_delete_books_authors_not_found(
    async_client: AsyncClient,
    test_book_in_db: BookInDB,
    test_author_in_db: AuthorInDB,
):
    relation = BooksAuthorsDelete(
        book_id=test_book_in_db.book_id,
        author_id=test_author_in_db.author_id,
    )
    response = await async_client.delete(
        f"/books_authors/delete?book_id={relation.book_id}&author_id={relation.author_id}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
