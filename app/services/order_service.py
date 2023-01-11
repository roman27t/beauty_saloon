import datetime as dt
from typing import Type

from models.order_model import OrderInSchema

from models import OrderModel, OrderDetailModel
from core.exceptions import ConflictError
from services.base_service import AbstractService

BOOKING_TIME_MINUTES = 15


class OrderService(AbstractService):
    @property
    def _table(self) -> Type[OrderModel]:
        return OrderModel

    async def add(self, schema: OrderInSchema) -> OrderModel:
        if not await self.__check_allow_times(schema=schema):
            raise ConflictError('already busy')
        schema_order = OrderModel.parse_obj(schema)
        schema_order.expired_at = dt.datetime.now() + dt.timedelta(minutes=BOOKING_TIME_MINUTES)
        return await super().add(schema=schema_order)

    async def __check_allow_times(self, schema: OrderInSchema) -> bool:
        return True


class OrderDetailService(AbstractService):
    @property
    def _table(self) -> Type[OrderDetailModel]:
        return OrderDetailModel
