from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.enums import ModulesEnum
from backend.src.volumes import schemas as volumes_schemas
from backend.src.volumes.deps import volume_exists_dep
from backend.src.volumes.models import VolumesModel
from backend.src.volumes.repository import VolumesRepository

router = APIRouter(
    prefix=f"/{ModulesEnum.VOLUMES.value}",
    tags=[ModulesEnum.VOLUMES],
)


@router.post(
    "/add",
    response_model=volumes_schemas.VolumeRead,
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


@router.delete(
    "/{volume_id}",
    response_model=volumes_schemas.VolumeRead,
    summary="Delete a volume.",
)
async def volumes_delete_by_id(
    existing_volume: Annotated[VolumesModel, Depends(volume_exists_dep)],
) -> VolumesModel:
    """Delete a volume by id."""
    return await VolumesRepository().delete_one(
        alchemy_model_to_delete=existing_volume,
    )
