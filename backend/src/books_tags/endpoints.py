from collections.abc import Sequence

from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import crud, http_exceptions
from backend.src.books_tags import crud as books_tags_crud
from backend.src.books_tags import schemas as books_tags_schemas
from backend.src.books_tags.models import BooksTagsModel
from backend.src.database import async_session_dependency
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.BOOKS_TAGS.value}",
    tags=[ModulesEnum.BOOKS_TAGS],
)


@router.get("/all", response_model=list[books_tags_schemas.BooksTagsRead])
async def books_tags_all(
    session: async_session_dependency,
) -> Sequence[BooksTagsModel]:
    books_tags_model = await crud.read_entities(
        alchemy_model=BooksTagsModel,
        session=session,
    )
    if not books_tags_model:
        raise http_exceptions.NotFound404
    return books_tags_model


@router.post(
    "/add",
    response_model=books_tags_schemas.BooksTagsRead,
    status_code=status.HTTP_201_CREATED,
)
async def books_tags_add(
    session: async_session_dependency,
    books_tags: books_tags_schemas.BooksTagsCreate,
) -> BooksTagsModel:
    try:
        return await crud.create_entity(
            alchemy_model=BooksTagsModel,
            pydantic_schema=books_tags,
            session=session,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e


@router.delete("/delete", response_model=books_tags_schemas.BooksTagsRead)
async def books_tags_delete(
    books_tags: books_tags_schemas.BooksTagsDelete,
    session: async_session_dependency,
) -> BooksTagsModel | None:
    return await books_tags_crud.delete_books_tags_by_id(
        books_tags=books_tags,
        session=session,
    )
