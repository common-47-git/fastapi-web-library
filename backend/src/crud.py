from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select

from backend.src.database import async_session_dependency
from backend.src.typing import CustomAlchemyModel


async def create_entity(
    alchemy_model: type[CustomAlchemyModel],
    pydantic_schema: BaseModel,
    session: async_session_dependency,
) -> CustomAlchemyModel:
    """Create one entry of a specified model in db."""
    new_entity = alchemy_model(**pydantic_schema.model_dump())
    session.add(new_entity)
    await session.commit()
    await session.refresh(new_entity)
    return new_entity


async def read_entity_by_field(
    alchemy_model: type[CustomAlchemyModel],
    field_name: str,
    field_value: Any,
    session: async_session_dependency,
) -> CustomAlchemyModel | None:
    """Read one entry of a specified model by a specified field from db."""
    query = select(alchemy_model).where(
        getattr(alchemy_model, field_name) == field_value,
    )
    result = await session.execute(query)
    return result.scalars().first()



async def read_entities(
    alchemy_model: type[CustomAlchemyModel],
    session: async_session_dependency,
) -> Sequence[CustomAlchemyModel]:
    """Read one entry of a specified model from db."""
    stmt = select(alchemy_model)
    result = await session.execute(stmt)
    return result.scalars().all()


async def delete_entity_by_field(
    alchemy_model: type[CustomAlchemyModel],
    field_name: str,
    field_value: Any,
    session: async_session_dependency,
) -> CustomAlchemyModel | None:
    """Delete one entry of a specified model by a specified field from db."""
    entity = await read_entity_by_field(
        alchemy_model=alchemy_model,
        field_name=field_name,
        field_value=field_value,
        session=session,
    )
    if not entity:
        return None
    await session.delete(entity)
    await session.commit()
    return entity
