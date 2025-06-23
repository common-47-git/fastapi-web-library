from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select

from backend.src.database import session_local
from backend.src.typing import CustomAlchemyModel


class AbstractRepository(ABC):
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
    async def delete_one_by_property():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    alchemy_model: type[CustomAlchemyModel]

    async def create_one(
        self,
        pydantic_schema: BaseModel,
    ):
        async with session_local() as session:
            new_entity = self.alchemy_model(**pydantic_schema.model_dump())
            session.add(new_entity)
            await session.commit()
            await session.refresh(new_entity)
            return new_entity

    async def read_one_by_property(self, field_name: str, field_value: Any):
        """Read one entry of a specified model by a specified field from db."""
        async with session_local() as session:
            query = select(self.alchemy_model).where(
                getattr(self.alchemy_model, field_name) == field_value,
            )
            result = await session.execute(query)
            return result.scalars().first()

    async def read_all(self):
        """Read one entry of a specified model from db."""
        async with session_local() as session:
            stmt = select(self.alchemy_model)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def delete_one_by_property(self, field_name: str, field_value: Any):
        """Delete one entry of a specified model by a specified field from db."""
        async with session_local() as session:
            entry = await self.read_one_by_property(
                field_name=field_name,
                field_value=field_value,
            )
            if not entry:
                return None
            await session.delete(entry)
            await session.commit()
            return entry
