from typing import Type, Union

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.base_models import BaseSQLModel
from models.database import get_session
from schemas.base_schema import BasePydanticSchema
from services import ServiceRegistry

T_SCHEMA = Union[BaseSQLModel, BasePydanticSchema]


def valid_empty_schema(class_schema: Type[T_SCHEMA]):
    def _valid_schema(schema: class_schema) -> class_schema:
        if not schema.dict(exclude_unset=True):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
        return schema
    return _valid_schema


class ValidGetByIdDependency:
    def __init__(self, model: Type[BaseSQLModel]):
        self.service_class = ServiceRegistry.get(model=model)

    async def __call__(self, pk: int, session: AsyncSession = Depends(get_session)) -> BaseSQLModel:
        return await self.service_class(db_session=session).get(pk=pk)
