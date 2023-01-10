from typing import Type

from models import OrderModel
from services.base_service import AbstractService


class OrderService(AbstractService):
    @property
    def _table(self) -> Type[OrderModel]:
        return OrderModel
