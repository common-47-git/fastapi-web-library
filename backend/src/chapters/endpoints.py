from fastapi import APIRouter, status

from backend.src import crud, status_codes
from backend.src.chapters import crud as chapter_crud
from backend.src.chapters import schemas as chapters_schemas
from backend.src.chapters.models import ChaptersModel
from backend.src.database import async_session_dependency

router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.post(
    "/add",
    response_model=chapters_schemas.ChapterCreate,
    status_code=status.HTTP_201_CREATED,
)
async def chapters_post_add(
    session: async_session_dependency,
    chapter: chapters_schemas.ChapterCreate,
):
    tags = await crud.create_entity(
        alchemy_model=ChaptersModel, pydantic_schema=chapter, session=session,
    )
    if not tags:
        raise status_codes.NotFound_404()
    return tags


@router.get("/read/{book_name}", response_model=chapters_schemas.ChapterRead)
async def books_get_read_by_name(
    session: async_session_dependency,
    book_name: str,
    volume: int = 1,
    chapter: int = 1,
):
    chapter = await chapter_crud.read_book_chapter(
        book_name=book_name,
        volume_number=volume,
        chapter_number=chapter,
        session=session,
    )

    if not chapter:
        raise status_codes.NotFound_404()
    return chapter
