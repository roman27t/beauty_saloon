from typing import Type

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from fastapi import status
from models import ClientModel
from schemas.user_schemas import ClientInSchema, ClientInOptionalSchema
from services.stub_init_service import LAST_NAMES
from tests.conftest import engine
from tests.utils import url_reverse, user_data


class TestUser:
    @property
    def _url_path(self) -> str:
        return 'client'

    @property
    def _model(self) -> Type[ClientModel]:
        return ClientModel

    @property
    def _in_schema(self) -> Type[ClientInSchema]:
        return ClientInSchema

    @property
    def _in_optional_schema(self) -> Type[ClientInOptionalSchema]:
        return ClientInOptionalSchema

    @property
    def _last_name(self) -> str:
        return LAST_NAMES[5]

    @pytest.mark.asyncio
    async def test_get_user_all(self, async_client: AsyncClient, async_session: AsyncSession):
        response = await async_client.get(url_reverse(f'view_get_{self._url_path}_all'))
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 5
        assert self._model(**content[0])


    @pytest.mark.parametrize('pk,status_code', [(1, status.HTTP_200_OK), (999, status.HTTP_404_NOT_FOUND)])
    @pytest.mark.asyncio
    async def test_get_user_by_id(self, async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int):
        response = await async_client.get(url_reverse(f'view_get_{self._url_path}_by_id', pk=pk))
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            employee = self._model(**response.json())
            assert employee.last_name == self._last_name


    @pytest.mark.parametrize(
        'is_error, status_code',
        [
            (False, status.HTTP_200_OK),
            (True, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ],
    )
    @pytest.mark.asyncio
    async def test_post_user(self, async_client: AsyncClient, async_session: AsyncSession, is_error: bool, status_code: int):
        employee_schema = self._in_schema(**user_data())
        content = '{}' if is_error else employee_schema.json()
        response = await async_client.post(url_reverse(f'view_add_{self._url_path}'), content=content)
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            result = await async_session.execute(
                select(ClientModel).where(ClientModel.last_name == employee_schema.last_name).limit(1)
            )
            user_db = result.scalars().first()
            assert user_db.last_name == employee_schema.last_name

    @pytest.mark.asyncio
    async def test_post_user_duplicate(self, async_client: AsyncClient, async_session: AsyncSession):
        for i in range(1,3):
            url = url_reverse(f'view_add_{self._url_path}')
            response = await async_client.post(url, content=self._in_schema(**user_data()).json())
            status_code = status.HTTP_200_OK if i == 1 else status.HTTP_422_UNPROCESSABLE_ENTITY
            assert response.status_code == status_code


    @pytest.mark.parametrize(
        'pk,data, status_code',
        [
            (1, {'first_name': 'Katerina'}, status.HTTP_200_OK),
            (1, {}, status.HTTP_400_BAD_REQUEST),
            (100, {'first_name': 'Katerina'}, status.HTTP_404_NOT_FOUND),
        ],
    )
    @pytest.mark.asyncio
    async def test_patch_user(
            self,
            async_client: AsyncClient,
            async_session: AsyncSession,
            pk: int,
            data: dict,
            status_code: int
    ):
        schema = self._in_optional_schema(**data)
        url = url_reverse(f'view_patch_{self._url_path}', pk=pk)
        response = await async_client.patch(url, content=schema.json(exclude_unset=True))
        await async_session.commit()
        assert response.status_code == status_code
        employee = self._model(**response.json())
        if status_code == status.HTTP_200_OK:
            session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
            async with session() as s:
                user_db = await s.get(self._model, employee.id)
                assert user_db.first_name == schema.first_name
