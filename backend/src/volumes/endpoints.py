from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.src import http_exceptions
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
    responses={
        201: http_exceptions.Created201().get_response_body(),
        409: http_exceptions.Conflict409().get_response_body(),
    },
)
async def post_volume(
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
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def delete_volume_by_id(
    existing_volume: Annotated[
        VolumesModel,
        Depends(VolumesDeps.one_exists),
    ], volume_id,
):
    """Delete a volume by id or raise 404."""
    return await VolumesServices().delete_one(alchemy_object=existing_volume)
