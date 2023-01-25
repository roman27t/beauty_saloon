import datetime as dt
from typing import Type

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload

from core.exceptions import ConflictException
from services.base_service import AbstractService
from entities.order.models_order import (
    OrderModel,
    OrderInSchema,
    OrderDetailModel,
)
from entities.service_name.models_service_name import ServiceNameModel
from entities.service_name.services_service_name import ServiceNameService

BOOKING_TIME_MINUTES = 15


class OrderService(AbstractService):
    @property
    def _table(self) -> Type[OrderModel]:
        return OrderModel

    async def add(self, schema: OrderInSchema) -> OrderModel:
        await self.__validations(schema=schema)
        schema_order = OrderModel.parse_obj(schema)
        schema_order.expired_at = dt.datetime.now() + dt.timedelta(minutes=BOOKING_TIME_MINUTES)
        order_model = await super().add(schema=schema_order)
        await self.__save_order_detail(order_model=order_model)
        return order_model

    async def __validations(self, schema: OrderInSchema):
        await self.__check_allow_times(schema=schema)

    async def __check_allow_times(self, schema: OrderInSchema):
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
        _id = await self.exists(conditions=or_(_conditions_1, _conditions_2))
        if bool(_id):
            raise ConflictException('already busy')

    async def __save_order_detail(self, order_model: OrderModel):
        service_model: ServiceNameModel = await ServiceNameService(db_session=self.db_session).get_by_filter(
            params={'id': order_model.service_id},
            options=[joinedload(ServiceNameModel.category)],
        )
        schema_detail = OrderDetailModel(
            order_id=order_model.id,
            category=service_model.category.name,
            name=service_model.name,
            detail=service_model.detail,
        )
        await OrderDetailService(db_session=self.db_session).add(schema=schema_detail)


class OrderDetailService(AbstractService):
    @property
    def _table(self) -> Type[OrderDetailModel]:
        return OrderDetailModel
