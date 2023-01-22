from typing import Dict, List, Union, Optional

from pydantic import condecimal

from models import OrderModel
from entities.service_name.models_service_name import ServiceNameModel
from entities.users.models_user import ClientModel, EmployeeModel
from models.choices import StatusOrder
from routers.choices import OrderFilter
from schemas.base_schema import PaginationSchema, BasePydanticSchema
from entities.category.schemas_category import CategoryInSchema
from core.utils.pagination import Pagination
from schemas.payment_schema import CardSchema, PaymentType


class OrderOptionalSchema(BasePydanticSchema):
    status: StatusOrder


class OrderPaymentSchema(BasePydanticSchema):
    p_type: PaymentType
    item: Union[CardSchema]
    price: condecimal(max_digits=7, decimal_places=2)


class OrderFullResponseSchema(BasePydanticSchema):
    user: Union['EmployeeModel', 'ClientModel']
    orders: List[OrderModel] = []
    users: Dict[int, Union['EmployeeModel', 'ClientModel']] = {}
    services: Dict[int, ServiceNameModel] = {}
    categories: Dict[int, CategoryInSchema] = {}
    pagination: Optional[PaginationSchema]

    @classmethod
    def build(cls, orders: List['OrderModel'], source: OrderFilter, pagination=Pagination) -> 'OrderFullResponseSchema':
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
