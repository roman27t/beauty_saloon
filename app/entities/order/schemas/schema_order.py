from typing import Union, Optional

from pydantic import condecimal

from schemas import PaginationSchema, BasePydanticSchema
from core.utils.pagination import Pagination
from entities.users.models_user import ClientModel, EmployeeModel
from entities.order.models_order import OrderModel
from entities.order.choices_order import OrderFilter, StatusOrder
from entities.category.schemas_category import CategoryInSchema
from entities.order.schemas.schema_payment import CardSchema, PaymentType
from entities.service_name.models_service_name import ServiceNameModel


class OrderOptionalSchema(BasePydanticSchema):
    status: StatusOrder


class OrderPaymentSchema(BasePydanticSchema):
    p_type: PaymentType
    item: Union[CardSchema]
    price: condecimal(max_digits=7, decimal_places=2)


class OrderFullResponseSchema(BasePydanticSchema):
    user: Union['EmployeeModel', 'ClientModel']
    orders: list[OrderModel] = []
    users: dict[int, Union['EmployeeModel', 'ClientModel']] = {}
    services: dict[int, ServiceNameModel] = {}
    categories: dict[int, CategoryInSchema] = {}
    pagination: Optional[PaginationSchema]

    @classmethod
    def build(cls, orders: list['OrderModel'], source: OrderFilter, pagination=Pagination) -> 'OrderFullResponseSchema':
        obj = cls(user=getattr(orders[0], source.value))
        for order in orders:
            user = getattr(order, source.invert())
            if user.id not in obj.users:
                obj.users[user.id] = user
            if order.service.id not in obj.services:
                obj.services[order.service.id] = order.service
                if order.service.category_id not in obj.categories:
                    obj.categories[order.service.category_id] = order.service.category
            obj.orders.append(order)
        obj.pagination = pagination.schema
        return obj
