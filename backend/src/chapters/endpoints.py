from fastapi import APIRouter, status

from backend.src import crud, http_exceptions
from backend.src.chapters import crud as chapter_crud
from backend.src.chapters import schemas as chapters_schemas
from backend.src.chapters.models import ChaptersModel
from backend.src.database import async_session_dependency
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.CHAPTERS.value}",
    tags=[ModulesEnum.CHAPTERS],
)


@router.post(
    "/add",
    response_model=chapters_schemas.ChapterCreate,
    status_code=status.HTTP_201_CREATED,
)
async def chapters_add(
    session: async_session_dependency,
    chapter: chapters_schemas.ChapterCreate,
) -> ChaptersModel:
    tags = await crud.create_entity(
        alchemy_model=ChaptersModel,
        pydantic_schema=chapter,
        session=session,
    )
    if not tags:
        raise http_exceptions.NotFound404
    return tags


@router.get("/read/{book_name}", response_model=chapters_schemas.ChapterRead)
async def books_get_read_by_name(
    session: async_session_dependency,
    book_name: str,
    volume_number: int = 1,
    chapter_number: int = 1,
) -> ChaptersModel | None:
    chapter = await chapter_crud.read_book_chapter(
        book_name=book_name,
        volume_number=volume_number,
        chapter_number=chapter_number,
        session=session,
    )

    if not chapter:
        raise http_exceptions.NotFound404
    return chapter
