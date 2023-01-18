from typing import Union, List, Dict

from pydantic import condecimal

from models import EmployeeModel, ClientModel, OrderModel, ServiceNameModel
from models.choices import StatusOrder
from models.service_model import CategoryInSchema
from routers.choices import OrderFilter
from schemas.base_schema import BasePydanticSchema
from schemas.payment_schema import CardSchema, PaymentType


class OrderOptionalSchema(BasePydanticSchema):
    status: StatusOrder


class OrderPaymentSchema(BasePydanticSchema):
    p_type: PaymentType
    item: Union[CardSchema]
    price: condecimal(max_digits=7, decimal_places=2)


class OrderFullResponseSchema(BasePydanticSchema):
    user: Union['EmployeeModel','ClientModel']
    orders: List[OrderModel] = []
    users: Dict[int, Union['EmployeeModel', 'ClientModel']] = {}
    services: Dict[int, ServiceNameModel] = {}
    categories: Dict[int, CategoryInSchema] = {}

    @classmethod
    def build(cls, orders: List['OrderModel'], source: OrderFilter) -> 'OrderFullResponseSchema':
        obj = cls(user=getattr(orders[0], source.value))
        for order in orders:
            user = getattr(order, source.invert())
            if user.id not in obj.users:
                obj.users[order.id] = user
            if order.service.id not in obj.services:
                obj.services[order.id] = order.service
                if order.service.category_id not in obj.categories:
                    obj.categories[order.service.category_id] = order.service.category
            obj.orders.append(order)
        return obj
