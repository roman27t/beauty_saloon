from abc import ABC, abstractmethod
from typing import Type, Union

import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from entities.users.models_user import ClientModel, EmployeeModel
from tests.utils import user_data, url_reverse
from tests.conftest import engine
from models.base_models import BaseSQLModel
from schemas import BasePydanticSchema


class UserAbstract(ABC):
    @property
    @abstractmethod
    def _url_path(self) -> str:
        ...

    @property
    @abstractmethod
    def _model(self) -> Type[BaseSQLModel]:
        ...

    @property
    @abstractmethod
    def _in_schema(self) -> Type[BasePydanticSchema]:
        ...

    @property
    @abstractmethod
    def _in_optional_schema(self) -> Type[BasePydanticSchema]:
        ...

    @property
    @abstractmethod
    def _last_name(self) -> str:
        ...

    @pytest.mark.asyncio
    async def test_get_user_all(self, async_client: AsyncClient, async_session: AsyncSession):
        response = await async_client.get(url_reverse(f'view_get_{self._url_path}_all'))
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 5
        assert self._model(**content[0])

    @pytest.mark.parametrize('pk,status_code', [(1, status.HTTP_200_OK), (999, status.HTTP_404_NOT_FOUND)])
    @pytest.mark.asyncio
    async def test_get_user_by_id(
        self, async_client: AsyncClient, async_session: AsyncSession, pk: int, status_code: int
    ):
        response = await async_client.get(url_reverse(f'view_get_{self._url_path}_by_id', pk=pk))
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            user: Union[EmployeeModel, ClientModel] = self._model(**response.json())
            assert user.last_name == self._last_name.lower()

    @pytest.mark.parametrize(
        'is_error, status_code',
        [
            (False, status.HTTP_200_OK),
            (True, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ],
    )
    @pytest.mark.asyncio
    async def test_post_user(
        self, async_client: AsyncClient, async_session: AsyncSession, is_error: bool, status_code: int
    ):
        user_schema = self._in_schema(**user_data())
        content = '{}' if is_error else user_schema.json()
        response = await async_client.post(url_reverse(f'view_add_{self._url_path}'), content=content)
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            result = await async_session.execute(
                select(self._model).where(self._model.last_name == user_schema.last_name).limit(1)
            )
            user_db = result.scalars().first()
            assert user_db.last_name == user_schema.last_name

    @pytest.mark.asyncio
    async def test_post_user_duplicate(self, async_client: AsyncClient, async_session: AsyncSession):
        for i in range(1, 3):
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
        self, async_client: AsyncClient, async_session: AsyncSession, pk: int, data: dict, status_code: int
    ):
        schema = self._in_optional_schema(**data)
        url = url_reverse(f'view_patch_{self._url_path}', pk=pk)
        response = await async_client.patch(url, content=schema.json(exclude_unset=True))
        await async_session.commit()
        assert response.status_code == status_code
        user = self._model(**response.json())
        if status_code == status.HTTP_200_OK:
            session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
            async with session() as s:
                user_db = await s.get(self._model, user.id)
                assert user_db.first_name == schema.first_name
