import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from config import i_config
from main import app
from core.utils.redis_interface import cache_redis
from services.stub_init_service import StubInitService

engine = create_async_engine(f'{i_config.DB_URL}', echo=False)
MOCK_FREEZE_TIME = '2023-1-16 09:30:00'


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=f'http://localhost:8000') as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def async_session() -> AsyncSession:
    await cache_redis.flushall()
    session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session() as s:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        await StubInitService(db_session=s).save_data_to_db()
        yield s

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()
