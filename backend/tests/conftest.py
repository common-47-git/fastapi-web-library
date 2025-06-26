from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import is_async_test
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from backend.env import db_config
from backend.main import app
from backend.src.database import BaseAlchemyModel, get_session


def pytest_collection_modifyitems(items):
    """Mark every test with pytest.mark.asyncio(loop_scope="session"). Overrides all manually added marks."""
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest_asyncio.fixture()
async def async_client() -> AsyncGenerator[AsyncClient]:
    db_url = f"postgresql+{db_config.DRIVER}://{db_config.LOGIN_USER}:{db_config.PASSWORD}@{db_config.SERVERNAME}/test_db"
    engine = create_async_engine(url=db_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(BaseAlchemyModel.metadata.create_all)

    test_session_local = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    async def override_get_session():
        session = test_session_local()
        try:
            yield session
        finally:
            await session.close()

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://test",
    ) as ac:
        yield ac

    async with engine.begin() as conn:
        await conn.run_sync(BaseAlchemyModel.metadata.drop_all)
    app.dependency_overrides.clear()
