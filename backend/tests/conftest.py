from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import is_async_test
from sqlalchemy.ext.asyncio import create_async_engine

from backend.env.config import DatabaseConfig
from backend.main import app
from backend.src.database import BaseAlchemyModel


def pytest_collection_modifyitems(items) -> None:
    """Mark every test with pytest.mark.asyncio(loop_scope="session"). Overrides all manually added marks."""
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest_asyncio.fixture()
async def async_client() -> AsyncGenerator[AsyncClient]:
    engine = create_async_engine(url=DatabaseConfig().pg_dsn, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(BaseAlchemyModel.metadata.create_all)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://test",
    ) as ac:
        yield ac

    async with engine.begin() as conn:
        await conn.run_sync(BaseAlchemyModel.metadata.drop_all)
