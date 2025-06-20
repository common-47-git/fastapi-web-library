from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from src import crud, status_codes
from src.books_tags import crud as books_tags_crud
from src.books_tags import schemas as books_tags_schemas
from src.books_tags.models import BooksTagsModel
from src.database import async_session_dependency

router = APIRouter(prefix="/books_tags", tags=["books_tags"])


@router.get("/all", response_model=list[books_tags_schemas.BooksTagsRead])
async def books_tags_all(
    session: async_session_dependency,
):
    books_tags_model = await crud.read_entities(
        alchemy_model=BooksTagsModel, session=session,
    )
    if not books_tags_model:
        raise status_codes.NotFound_404()
    return books_tags_model


@router.post(
    "/add",
    response_model=books_tags_schemas.BooksTagsRead,
    status_code=status.HTTP_201_CREATED,
)
async def books_tags_add(
    session: async_session_dependency,
    books_tags: books_tags_schemas.BooksTagsCreate,
):
    try:
        entity = await crud.create_entity(
            alchemy_model=BooksTagsModel,
            pydantic_schema=books_tags,
            session=session,
        )
        return entity
    except IntegrityError as e:
        raise status_codes.Conflict_409(exception=e)


@router.delete("/delete", response_model=books_tags_schemas.BooksTagsRead)
async def books_tags_delete(
    books_tags: books_tags_schemas.BooksTagsDelete,
    session: async_session_dependency,
):
    return await books_tags_crud.delete_books_tags_by_id(
        books_tags=books_tags, session=session,
    )
