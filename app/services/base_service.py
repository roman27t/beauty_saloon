from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Type, Union, TypeVar, Optional

from fastapi import HTTPException, status
from sqlmodel import func
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import BasePydanticSchema
from models.db_helper import db_commit
from models.base_models import BaseSQLModel

if TYPE_CHECKING:
    from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

MODEL = TypeVar('MODEL', bound=BaseSQLModel)
SCHEMA = TypeVar('SCHEMA', bound=BasePydanticSchema)
TYPE_CONDITIONS = Union['BinaryExpression', 'BooleanClauseList']


class BaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.init()

    def init(self):
        pass


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

    async def get(self, pk: int, e_message: str = '', raise_ex: bool = True) -> Optional[MODEL]:
        obj_db = await self.db_session.get(self._table, pk)
        if raise_ex and not obj_db:
            e_message = e_message or f'item with id {pk} not found'
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e_message)
        return obj_db

    async def exists(self, conditions: Union['BinaryExpression', 'BooleanClauseList']) -> Optional[int]:
        result = await self.db_session.execute(select(self._table.id).where(conditions).limit(1))
        data: Optional[int] = result.scalar()
        return data

    async def get_by_filter(self, params: dict, options: Optional[List] = None) -> MODEL:
        objs_db = await self.filter(params=params, options=options, limit=1)
        if not objs_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='item not found')
        return objs_db[0]

    async def count(self, params: dict) -> int:
        query = select(func.count(self._table.id)).where(*self.parse_params(params=params))
        result = await self.db_session.execute(query)
        return result.scalar()

    async def filter(
        self,
        params: Union[dict, List[TYPE_CONDITIONS]],
        options: Optional[List] = None,
        joins: Optional[List] = None,
        limit: int = 0,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
    ) -> List[MODEL]:
        params = self.parse_params(params=params) if isinstance(params, dict) else params
        query = select(self._table).options(*options or []).where(*params)
        for model_join in joins or []:
            query = query.join(model_join)
        if order_by:
            query = query.order_by(desc(order_by[1:]) if order_by.startswith('-') else order_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    def parse_params(self, params: dict) -> list:
        return [getattr(self._table, key) == value for key, value in params.items()]
