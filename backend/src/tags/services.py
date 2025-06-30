from backend.src.services import BaseServices
from backend.src.tags.models import TagsModel
from backend.src.tags.repository import TagsRepository


class TagsServices(BaseServices):
    alchemy_model: type[TagsModel] = TagsModel
    repository: type[TagsRepository] = TagsRepository
