import uuid

from backend.src.authors.models import AuthorsModel
from backend.src.authors.services import AuthorsServices


class AuthorsDeps:
    @staticmethod
    async def one_exists(author_id: uuid.UUID) -> AuthorsModel:
        return await AuthorsServices().read_one_by_property(
            property_name=AuthorsModel.author_id.key,
            property_value=author_id,
        )
