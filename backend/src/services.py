from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.src import http_exceptions
from backend.src.database import BaseAlchemyModel
from backend.src.repository import SQLAlchemyRepository


class AbstractServices(ABC):
    @abstractmethod
    async def create_one():
        raise NotImplementedError

    @abstractmethod
    async def read_one_by_property():
        raise NotImplementedError

    @abstractmethod
    async def read_all():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one_by_property():
        raise NotImplementedError


class BaseServices:
    repository: type[SQLAlchemyRepository]
    alchemy_model: type[BaseAlchemyModel]

    async def create_one(self, pydantic_schema: BaseModel):
        try:
            new_alchemy_object = self.alchemy_model(
                **pydantic_schema.model_dump(),
            )
            return await self.repository().create_one(
                alchemy_object=new_alchemy_object,
            )
        except IntegrityError as e:
            raise http_exceptions.Conflict409(exception=e) from e

    async def read_one_by_property(
        self,
        property_name: str,
        property_value: Any,
    ):
        entry = await self.repository().read_one_by_property(
            property_name=property_name,
            property_value=property_value,
        )
        if entry is None:
            raise http_exceptions.NotFound404
        return entry

    async def read_all(self):
        entries = await self.repository().read_all()
        if not entries:
            raise http_exceptions.NotFound404
        return entries

    async def delete_one(
        self,
        alchemy_object: BaseAlchemyModel,
    ):
        return await self.repository().delete_one(
            alchemy_object_to_delete=alchemy_object,
        )

    async def delete_one_by_property(
        self,
        property_name: str,
        property_value: Any,
    ):
        deleted = await self.repository().delete_one_by_property(
            property_name=property_name,
            property_value=property_value,
        )
        if not deleted:
            raise http_exceptions.NotFound404
        return deleted
