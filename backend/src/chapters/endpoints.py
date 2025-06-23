from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.chapters import schemas as chapters_schemas
from backend.src.chapters.models import ChaptersModel
from backend.src.chapters.repository import ChaptersRepository
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.CHAPTERS.value}",
    tags=[ModulesEnum.CHAPTERS],
)


@router.post(
    "/add",
    response_model=chapters_schemas.ChapterCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Add a chapter to a volume.",
)
async def chapters_add(
    chapter: chapters_schemas.ChapterCreate,
):
    """Add a chapter to an existing volume linked by volume_id."""
    try:
        entry = await ChaptersRepository().create_one(
            pydantic_schema=chapter,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e
    else:
        return entry


@router.get(
    "/read/{book_name}",
    response_model=chapters_schemas.ChapterRead,
    summary="Read a chapter.",
)
async def books_get_read_by_name(
    book_name: str,
    volume_number: int = 1,
    chapter_number: int = 1,
) -> ChaptersModel | None:
    """Read a chapter linked with book by volume_id and book_id."""
    chapter = await ChaptersRepository().read_book_chapter(
        book_name=book_name,
        volume_number=volume_number,
        chapter_number=chapter_number,
    )
    if not chapter:
        raise http_exceptions.NotFound404
    return chapter
