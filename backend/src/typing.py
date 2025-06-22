from typing import TypeVar

from backend.src.database import BaseAlchemyModel

CustomAlchemyModel = TypeVar("CustomAlchemyModel", bound=BaseAlchemyModel)
