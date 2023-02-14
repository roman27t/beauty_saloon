from typing import Type, Union, Callable

from fastapi import Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import BasePydanticSchema
from models.database import get_session
from models.base_models import BaseSQLModel
from services.base_service import AbstractService

T_SCHEMA = Union[BaseSQLModel, BasePydanticSchema]


def valid_empty_schema(class_schema: Type[T_SCHEMA]) -> Callable[[Type[T_SCHEMA]], Type[T_SCHEMA]]:
    def _valid_schema(schema: class_schema) -> class_schema:
        if not schema.dict(exclude_unset=True):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
        return schema

    return _valid_schema


class ValidOrderByDependency:
    def __init__(self, class_schema: Type[T_SCHEMA]):
        self.class_schema = class_schema

    def __call__(self, order_by: str = '') -> str:
        field_order_by = order_by[1:] if order_by.startswith('-') else order_by
        if field_order_by and field_order_by not in self.class_schema.schema()['required']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='wrong field')
        return order_by


class ValidGetByIdDependency:
    def __init__(self, class_service: Type[AbstractService]):
        self.class_service = class_service

    async def __call__(self, pk: int, session: AsyncSession = Depends(get_session)) -> BaseSQLModel:
        return await self.class_service(db_session=session).get(pk=pk)
