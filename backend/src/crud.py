from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select

from backend.src.database import Base, async_session_dependency


async def create_entity(
    alchemy_model: type[Base],
    pydantic_schema: BaseModel,
    session: async_session_dependency,
) -> Base:
    new_entity = alchemy_model(**pydantic_schema.model_dump())
    session.add(new_entity)
    await session.commit()
    await session.refresh(new_entity)
    return new_entity


async def read_entity_by_field(
    alchemy_model: type[Base],
    field_name: str,
    field_value: Any,
    session: async_session_dependency,
) -> Base | None:
    query = select(alchemy_model).where(
        getattr(alchemy_model, field_name) == field_value,
    )
    result = await session.execute(query)
    return result.scalars().first()


async def read_entities(
    alchemy_model: type[Base], session: async_session_dependency,
) -> Sequence[Base] | None:
    stmt = select(alchemy_model)
    result = await session.execute(stmt)
    return result.scalars().all()


async def delete_entity_by_field(
    alchemy_model: type[Base],
    field_name: str,
    field_value: Any,
    session: async_session_dependency,
) -> Base | None:
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
