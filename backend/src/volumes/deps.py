import uuid

from backend.src import http_exceptions
from backend.src.volumes.models import VolumesModel
from backend.src.volumes.repository import VolumesRepository


class VolumesDeps:
    @staticmethod
    async def one_exists(volume_id: uuid.UUID) -> VolumesModel:
        volume = await VolumesRepository().read_one_by_property(
            property_name=VolumesModel.volume_id.key,
            property_value=volume_id,
        )
        if volume is None:
            raise http_exceptions.NotFound404
        return volume
