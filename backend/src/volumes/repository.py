from backend.src.repository import SQLAlchemyRepository
from backend.src.volumes.models import VolumesModel


class VolumesRepository(SQLAlchemyRepository):
    alchemy_model: type[VolumesModel] = VolumesModel
