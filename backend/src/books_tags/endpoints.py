import uuid

from fastapi import APIRouter, status

from backend.src.books_tags import schemas as books_tags_schemas
from backend.src.books_tags.services import BooksTagsServices
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
async def books_tags_all():
    """Get a list of entries book_id-tag_id."""
    return await BooksTagsServices().read_all()


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
    return await BooksTagsServices().create_one(
        pydantic_schema=books_tags,
    )


@router.delete(
    "/delete",
    response_model=books_tags_schemas.BooksTagsRead,
    summary="Delete a book-tag entry.",
)
async def books_tags_delete(
    book_id: uuid.UUID,
    tag_id: uuid.UUID,
):
    return await BooksTagsServices().delete_books_tags_by_id(
        books_tags=books_tags_schemas.BooksTagsDelete(
            book_id=book_id,
            tag_id=tag_id,
        ),
    )
