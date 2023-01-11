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

    async def add(self, schema: OrderInSchema):
        if not await self.__check_allow_times(schema=schema):
            raise ConflictError('already busy')
        await super().add(schema=schema)

    async def __check_allow_times(self, schema: OrderInSchema) -> bool:
        return True


class OrderDetailService(AbstractService):
    @property
    def _table(self) -> Type[OrderDetailModel]:
        return OrderDetailModel
