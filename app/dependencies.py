from typing import Callable, Type, Union

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


def valid_group_by(class_schema: Type[T_SCHEMA]):
    def _valid_group_by(order_by: str = '', class_schema_: Type[T_SCHEMA] = class_schema) -> str:
        field_order_by = order_by[1:] if order_by.startswith('-') else order_by
        if field_order_by and field_order_by not in class_schema_.schema()['required']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='wrong field')
        return order_by

    return _valid_group_by


class ValidGetByIdDependency:
    def __init__(self, class_service: Type[AbstractService]):
        self.class_service = class_service

    async def __call__(self, pk: int, session: AsyncSession = Depends(get_session)) -> BaseSQLModel:
        return await self.class_service(db_session=session).get(pk=pk)
