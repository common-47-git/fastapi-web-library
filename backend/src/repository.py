from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select

from backend.src.database import BaseAlchemyModel, session_local


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self):
        raise NotImplementedError

    @abstractmethod
    async def read_one_by_property(self):
        raise NotImplementedError

    @abstractmethod
    async def read_all(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_one_by_property(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    alchemy_model: type[BaseAlchemyModel]

    async def create_one(
        self,
        alchemy_object: BaseAlchemyModel,
    ):
        """Create one entry of a specified model in db."""
        async with session_local() as session:
            session.add(alchemy_object)
            await session.commit()
            await session.refresh(alchemy_object)
            return alchemy_object

    async def read_one_by_property(
        self,
        property_name: str,
        property_value: Any,
    ):
        """Read one entry of a specified model by a specified field from db."""
        async with session_local() as session:
            query = select(self.alchemy_model).where(
                getattr(self.alchemy_model, property_name) == property_value,
            )
            result = await session.execute(query)
            return result.scalars().first()

    async def read_all(self):
        """Read one entry of a specified model from db."""
        async with session_local() as session:
            stmt = select(self.alchemy_model)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def delete_one(
        self,
        alchemy_object_to_delete: BaseAlchemyModel,
    ):
        """Delete one entry of a given specified model."""
        async with session_local() as session:
            await session.delete(alchemy_object_to_delete)
            await session.commit()
            return alchemy_object_to_delete

    async def delete_one_by_property(
        self,
        property_name: str,
        property_value: Any,
    ):
        """Delete one entry of a specified model by a specified field from db."""
        async with session_local() as session:
            entry = await self.read_one_by_property(
                property_name=property_name,
                property_value=property_value,
            )
            if entry is None:
                return None
            await session.delete(entry)
            await session.commit()
            return entry
