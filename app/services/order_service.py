from typing import Type

from core.exceptions import ConflictError
from models import OrderModel
from services.base_service import AbstractService

BOOKING_TIME_MINUTES = 15


class OrderService(AbstractService):
    @property
    def _table(self) -> Type[OrderModel]:
        return OrderModel

    async def add(self, schema):    # todo schema
        if not await self.__check_allow_times(schema=schema):
            raise ConflictError('already busy')
        await super().add(schema=schema)

    async def __check_allow_times(self, schema) -> bool:
        return True
