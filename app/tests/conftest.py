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
from app.main import app
from models.db_helper import db_commit
from services.stub_init_service import StubInitService

engine = create_async_engine(f'{i_config.DB_URL}', echo=False)


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=f'http://localhost:8000') as client:  # {settings.api_v1_prefix}
        yield client


@pytest_asyncio.fixture(scope='function')
async def async_session() -> AsyncSession:
    session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session() as s:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        StubInitService(db_session=s).init()
        await db_commit(db_session=s)
        yield s

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


# @pytest.fixture(scope='function')
# def test_data() -> dict:
#    path = os.getenv('PYTEST_CURRENT_TEST')
#    path = os.path.join(*os.path.split(path)[:-1], 'data', 'data.json')
#
#    if not os.path.exists(path):
#        path = os.path.join('data', 'data.json')
#
#    with open(path, 'r') as file:
#        data = json.loads(file.read())
#
#    return data
