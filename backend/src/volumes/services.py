from backend.src.services import BaseServices
from backend.src.volumes.models import VolumesModel
from backend.src.volumes.repository import VolumesRepository


class VolumesServices(BaseServices):
    alchemy_model: type[VolumesModel] = VolumesModel
    repository: type[VolumesRepository] = VolumesRepository
