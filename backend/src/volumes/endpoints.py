from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.src.enums import ModulesEnum
from backend.src.volumes import schemas as volumes_schemas
from backend.src.volumes.deps import VolumesDeps
from backend.src.volumes.models import VolumesModel
from backend.src.volumes.services import VolumesServices

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
    return await VolumesServices().create_one(
        pydantic_schema=volume,
    )


@router.delete(
    "/{volume_id}",
    response_model=volumes_schemas.VolumeRead,
    summary="Delete a volume.",
)
async def volumes_delete_by_id(
    existing_volume: Annotated[
        VolumesModel,
        Depends(VolumesDeps.one_exists),
    ],
):
    """Delete a volume by id or raise 404."""
    return await VolumesServices().delete_one(alchemy_object=existing_volume)
