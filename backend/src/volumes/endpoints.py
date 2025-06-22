from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from backend.src import crud, http_exceptions
from backend.src.database import async_session_dependency
from backend.src.enums import ModulesEnum
from backend.src.volumes import schemas as volumes_schemas
from backend.src.volumes.models import VolumesModel

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
    session: async_session_dependency,
    volume: volumes_schemas.VolumeCreate,
) -> VolumesModel:
    """Add a volume to a book linked by book_id."""
    try:
        entity = await crud.create_entity(
            alchemy_model=VolumesModel,
            pydantic_schema=volume,
            session=session,
        )
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e
    else:
        return entity
