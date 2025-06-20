from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from env.config import DBNAME, LOGIN_USER, PASSWORD, SERVERNAME

db_url = f"postgresql+asyncpg://{LOGIN_USER}:{PASSWORD}@{SERVERNAME}/{DBNAME}"

engine = create_async_engine(url=db_url, echo=True)

session_local = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine,
)


async def get_session():
    session = session_local()
    try:
        yield session
    finally:
        await session.close()


async_session_dependency = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    _columns_values = ""
    _columns_to_show = 2

    def __repr__(self) -> str:
        for _, column in enumerate(self.__table__.c):
            if _ < self._columns_to_show:
                self._columns_values += f"{column.key}={getattr(self, column.key)} "
            else:
                continue
        return f"{self.__tablename__}({self._columns_values.strip()})"
