
from backend.src.repository import SQLAlchemyRepository
from backend.src.users.models import UsersModel


class UsersRepository(SQLAlchemyRepository):
    alchemy_model: type[UsersModel] = UsersModel
