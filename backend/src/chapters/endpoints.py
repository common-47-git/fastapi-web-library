import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.src import http_exceptions
from backend.src.chapters import schemas as chapters_schemas
from backend.src.chapters.deps import ChaptersDeps
from backend.src.chapters.models import ChaptersModel
from backend.src.chapters.services import ChaptersServices
from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.CHAPTERS.value}",
    tags=[ModulesEnum.CHAPTERS],
)


@router.post(
    "/add",
    response_model=chapters_schemas.ChapterRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a chapter to a volume.",
    responses={
        201: http_exceptions.Created201().get_response_body(),
        409: http_exceptions.Conflict409().get_response_body(),
    },
)
async def post_chapter(
    chapter: chapters_schemas.ChapterCreate,
):
    """Add a chapter to an existing volume linked by volume_id."""
    return await ChaptersServices().create_one(pydantic_schema=chapter)


@router.get(
    "/read/{book_name}",
    response_model=chapters_schemas.ChapterRead,
    summary="Read a chapter.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_chapter_by_book_name(
    book_name: str,
    volume_number: int = 1,
    chapter_number: int = 1,
):
    """Read a chapter linked with book by volume_id and book_id."""
    return await ChaptersServices().read_book_chapter_by_book_name(
        book_name=book_name,
        volume_number=volume_number,
        chapter_number=chapter_number,
    )


@router.get(
    "/read-id/{book_id}",
    response_model=chapters_schemas.ChapterRead,
    summary="Read a chapter.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_chapter_by_book_id(
    book_id: uuid.UUID,
    volume_number: int = 1,
    chapter_number: int = 1,
):
    """Read a chapter linked with book by volume_id and book_id."""
    return await ChaptersServices().read_book_chapter_by_book_id(
        book_id=book_id,
        volume_number=volume_number,
        chapter_number=chapter_number,
    )


@router.delete(
    "/{chapter_id}",
    response_model=chapters_schemas.ChapterRead,
    summary="Delete a chapter.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def delete_chapter_by_id(
    existing_chapter: Annotated[
        ChaptersModel,
        Depends(ChaptersDeps.one_exists),
    ],
    chapter_id,
):
    """Delete a chapter by id or raise 404."""
    return await ChaptersServices().delete_one(
        alchemy_object=existing_chapter,
    )
