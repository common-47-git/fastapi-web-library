import uuid
from collections.abc import Sequence

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.books_tags import schemas as books_tags_schemas
from backend.src.books_tags.models import BooksTagsModel
from backend.src.books_tags.repository import BooksTagsRepository
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.BOOKS_TAGS.value}",
    tags=[ModulesEnum.BOOKS_TAGS],
)


@router.get(
    "/all",
    response_model=list[books_tags_schemas.BooksTagsRead],
    summary="Get a list of books and tags.",
)
async def books_tags_all() -> Sequence[BooksTagsModel]:
    """Get a list of entries book_id-tag_id."""
    books_tags_model = await BooksTagsRepository().read_all()
    if not books_tags_model:
        raise http_exceptions.NotFound404
    return books_tags_model


@router.post(
    "/add",
    response_model=books_tags_schemas.BooksTagsRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book-tag entry.",
)
async def books_tags_add(
    books_tags: books_tags_schemas.BooksTagsCreate,
):
    """Create an entry book_id-tag_id."""
    try:
        return await BooksTagsRepository().create_one(
            pydantic_schema=books_tags,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete(
    "/delete",
    response_model=books_tags_schemas.BooksTagsRead,
    summary="Delete a book-tag entry.",
)
async def books_tags_delete(
    book_id: uuid.UUID,
    tag_id: uuid.UUID,
) -> BooksTagsModel:
    deleted = await BooksTagsRepository().delete_books_tags_by_id(
        books_tags=books_tags_schemas.BooksTagsDelete(
            book_id=book_id,
            tag_id=tag_id,
        ),
    )
    if not deleted:
        raise http_exceptions.NotFound404
    return deleted
