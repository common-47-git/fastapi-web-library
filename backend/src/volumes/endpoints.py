from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError

from backend.src.enums import ModulesEnum
from backend.src.volumes import schemas as volumes_schemas
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
    volume_id: uuid.UUID,
):
    """Delete a volume by id."""
    return await VolumesServices().delete_one_by_property(
        property_name=VolumesModel.volume_id.key,
        property_value=volume_id,
    )
