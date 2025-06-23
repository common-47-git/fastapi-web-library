from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.enums import ModulesEnum
from backend.src.volumes import schemas as volumes_schemas
from backend.src.volumes.repository import VolumesRepository

router = APIRouter(
    prefix=f"/{ModulesEnum.VOLUMES.value}",
    tags=[ModulesEnum.VOLUMES],
)


@router.post(
    "/add",
    response_model=volumes_schemas.VolumeCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Add a volume to a book.",
)
async def volumes_add(
    volume: volumes_schemas.VolumeCreate,
):
    """Add a volume to a book linked by book_id."""
    try:
        entity = await VolumesRepository().create_one(
            pydantic_schema=volume,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e
    else:
        return entity
