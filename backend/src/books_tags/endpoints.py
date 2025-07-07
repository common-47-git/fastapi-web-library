from typing import Annotated

from fastapi import APIRouter, Query, status

from backend.src import http_exceptions
from backend.src.books_tags import schemas as books_tags_schemas
from backend.src.books_tags.services import BooksTagsServices
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.BOOKS_TAGS.value}",
    tags=[ModulesEnum.BOOKS_TAGS],
)


@router.get(
    "/",
    response_model=list[books_tags_schemas.BooksTagsRead],
    summary="Get a list of books and tags.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_all_books_tags():
    """Get a list of entries book_id-tag_id."""
    return await BooksTagsServices().read_all()


@router.post(
    "/add",
    response_model=books_tags_schemas.BooksTagsRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book-tag entry.",
    responses={
        201: http_exceptions.Created201().get_response_body(),
        409: http_exceptions.Conflict409().get_response_body(),
    },
)
async def post_book_tag(
    books_tags: books_tags_schemas.BooksTagsCreate,
):
    """Create an entry book_id-tag_id."""
    return await BooksTagsServices().create_one(
        pydantic_schema=books_tags,
    )


@router.delete(
    "/delete",
    response_model=books_tags_schemas.BooksTagsRead,
    summary="Delete a book-tag entry.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def delete_book_tag(
    book_tag: Annotated[books_tags_schemas.BooksTagsDelete, Query()],
):
    """Delete an entry book_id-author_id or raise 404."""
    return await BooksTagsServices().delete_books_tags_by_id(
        books_tags=book_tag,
    )
