from abc import ABC, abstractmethod
from typing import Type

from models.db_helper import db_commit
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


class BaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


class BaseService2(ABC):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @property
    @abstractmethod
    def _table(self) -> Type[SQLModel]:
        pass

    def add_async(self, schema: PydanticBaseModel):  # : EmployeeInSchema
        obj_db = self._table(**schema.dict())
        self.db_session.add(obj_db)
        return obj_db

    async def add(self, schema: PydanticBaseModel):  # : EmployeeInSchema
        obj_db = self.add_async(schema=schema)
        await db_commit(db_session=self.db_session, message=f'The {self._table.__class__} is already stored')
        return obj_db
    
    async def update(self, obj_db, schema: PydanticBaseModel): # : EmployeeModel,  : EmployeeInSchema
        for key, value in schema.dict(exclude_unset=True).items():
            setattr(obj_db, key, value)
        self.db_session.add(obj_db)
        await self.db_session.commit()
        await self.db_session.refresh(obj_db)

    async def get_all(self) -> list:    # [EmployeeModel]
        result = await self.db_session.execute(
            select(self._table).order_by(getattr(self._table, 'id')).limit(20)  # (ClientModel.last_name.desc())
        )
        return result.scalars().all()

    async def get(self, pk: int):   #  -> EmployeeModel
        result = await self.db_session.get(self._table, pk)
        return result
