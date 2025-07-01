import uuid

from backend.src import http_exceptions
from backend.src.users.models import UsersModel
from backend.src.users.repository import UsersRepository


class UsersDeps:
    @staticmethod
    async def one_exists(user_id: uuid.UUID) -> UsersModel:
        user = await UsersRepository().read_one_by_property(
            property_name=UsersModel.user_id.key,
            property_value=user_id,
        )
        if user is None:
            raise http_exceptions.NotFound404
        return user
