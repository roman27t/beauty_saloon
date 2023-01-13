import datetime as dt
from typing import Type, Optional

from models import OrderModel, OrderDetailModel
from core.exceptions import ConflictException
from models.order_model import OrderInSchema
from services.base_service import AbstractService

BOOKING_TIME_MINUTES = 15


class OrderService(AbstractService):
    @property
    def _table(self) -> Type[OrderModel]:
        return OrderModel

    async def add(self, schema: OrderInSchema) -> OrderModel:
        await self.__validations(schema=schema)
        schema_order = OrderModel.parse_obj(schema)
        schema_order.expired_at = dt.datetime.now() + dt.timedelta(minutes=BOOKING_TIME_MINUTES)
        return await super().add(schema=schema_order)

    async def __validations(self, schema: OrderInSchema):
        await self.__check_allow_times(schema=schema)

    async def __check_allow_times(self, schema: OrderInSchema):
        # todo --> exists()
        from sqlalchemy import or_, and_, select

        _conditions_1 = and_(
            OrderModel.employee_id == schema.employee_id,
            OrderModel.start_at >= schema.start_at,
            OrderModel.end_at <= schema.end_at,
        )
        _conditions_2 = and_(
            OrderModel.employee_id == schema.employee_id,
            OrderModel.start_at < schema.end_at,
            OrderModel.end_at > schema.end_at,
        )
        result = await self.db_session.execute(select(self._table.id).where(or_(_conditions_1, _conditions_2)).limit(1))
        data: Optional[int] = result.scalar()
        if bool(data):
            raise ConflictException('already busy')


class OrderDetailService(AbstractService):
    @property
    def _table(self) -> Type[OrderDetailModel]:
        return OrderDetailModel
