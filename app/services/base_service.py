from abc import ABC, abstractmethod
from typing import List, Type, TypeVar, TYPE_CHECKING, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base_models import BaseSQLModel
from models.db_helper import db_commit
from schemas.base_schema import BasePydanticSchema

if TYPE_CHECKING:
    from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

MODEL = TypeVar('MODEL', bound=BaseSQLModel)
SCHEMA = TypeVar('SCHEMA', bound=BasePydanticSchema)


class BaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


class AbstractService(BaseService, ABC):
    @property
    @abstractmethod
    def _table(self) -> Type[BaseSQLModel]:
        pass

    @property
    def name(self) -> str:
        return self._table.__table__.name

    def pre_add(self, schema: SCHEMA) -> MODEL:
        obj_db = self._table(**schema.dict())
        self.db_session.add(obj_db)
        return obj_db

    async def add(self, schema: SCHEMA) -> MODEL:
        obj_db = self.pre_add(schema=schema)
        await db_commit(db_session=self.db_session, message=f'The {self.name} is already stored')
        return obj_db

    async def update(self, obj_db, schema: SCHEMA):
        for key, value in schema.dict(exclude_unset=True).items():
            setattr(obj_db, key, value)
        self.db_session.add(obj_db)
        await self.db_session.commit()
        await self.db_session.refresh(obj_db)

    async def get_all(self) -> list[MODEL]:
        result = await self.db_session.execute(select(self._table).order_by(getattr(self._table, 'id')))
        return result.scalars().all()

    async def get(self, pk: int) -> Optional[MODEL]:
        result = await self.db_session.get(self._table, pk)
        return result

    async def exists(self, conditions: Union['BinaryExpression', 'BooleanClauseList']) -> Optional[int]:
        result = await self.db_session.execute(select(self._table.id).where(conditions).limit(1))
        data: Optional[int] = result.scalar()
        return data

    async def filter(self, params: dict) -> List[MODEL]:
        result = await self.db_session.execute(select(self._table).where(*self.__parse_params(params=params)))
        return result.scalars().all()

    def __parse_params(self, params: dict) -> list:
        return [getattr(self._table, key) == value for key, value in params.items()]
