from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from backend.env import db_config

engine = create_async_engine(url=db_config.pg_dsn, echo=True)

session_local = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def get_session():
    session = session_local()
    try:
        yield session
    finally:
        await session.close()


class BaseAlchemyModel(DeclarativeBase):
    _columns_values = ""
    _columns_to_show = 2

    def __repr__(self) -> str:
        """Return string representation of a model with limited columns."""
        for i, column in enumerate(self.__table__.c):
            if i < self._columns_to_show:
                self._columns_values += (
                    f"{column.key}={getattr(self, column.key)} "
                )
            else:
                continue
        return f"{self.__tablename__}({self._columns_values.strip()})"
