import datetime as dt
from decimal import Decimal
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import ValidGetByIdDependency
from models.database import get_session
from entities.offer.models_offer import OfferModel
from entities.order.models_order import OrderModel, OrderInSchema
from entities.order.choices_order import StatusOrder
from entities.offer.services_offer import OfferService
from entities.order.services_order import OrderService
from entities.order.schemas.schema_order import OrderPaymentSchema
from entities.users.services.client_service import ClientService
from entities.service_name.models_service_name import ServiceNameModel


def _check_status_wait_core(obj_db: OrderModel):
    if obj_db.status != StatusOrder.WAIT:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='status order already expired')


async def valid_status_wait(obj_db: OrderModel = Depends(ValidGetByIdDependency(OrderService))) -> OrderModel:
    _check_status_wait_core(obj_db=obj_db)
    return obj_db


@dataclass
class ValidPostOrderDependency:
    schema: OrderInSchema
    session: AsyncSession = Depends(get_session)

    async def __call__(self) -> OrderInSchema:
        self.offer_db = await self.__check_get_offer_db()
        self.__check_active_service_category()
        self.__check_price()
        await self.__check_client()
        return self.schema

    async def __check_get_offer_db(self) -> OfferModel:
        if not self.schema.dict(exclude_unset=True):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
        params = {'service_name_id': self.schema.service_id, 'employee_id': self.schema.employee_id, 'is_active': True}
        options = [selectinload(OfferModel.service_name).joinedload(ServiceNameModel.category)]
        return await OfferService(db_session=self.session).get_by_filter(params=params, options=options)

    def __check_active_service_category(self):
        if not self.offer_db.service_name.is_active:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='service already disabled')
        if not self.offer_db.service_name.category.is_active:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='category already disabled')

    async def __check_client(self):
        pk = self.schema.client_id
        await ClientService(db_session=self.session).get(pk=self.schema.client_id, e_message=f'client {pk} not found')

    def __check_price(self):
        origin_price = count_price(
            price=self.offer_db.service_name.price,
            rate=self.offer_db.rate,
            start_at=self.schema.start_at,
            end_at=self.schema.end_at,
        )
        _check_price(origin_price=origin_price, client_price=self.schema.price)


def count_price(price: Decimal, rate: Decimal, start_at: dt.datetime, end_at: dt.datetime) -> Decimal:
    _price = price * rate
    _parts = Decimal((end_at - start_at).total_seconds() / 60 / 30)
    return (_price * _parts).normalize()


def _check_price(origin_price: Decimal, client_price: Decimal):
    if origin_price != client_price:
        message = f'price error {origin_price} != {client_price}'
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)


@dataclass
class ValidPaymentOrderDependency:
    pk: int
    schema: OrderPaymentSchema
    session: AsyncSession = Depends(get_session)

    async def __call__(self) -> OrderModel:
        obj_db: OrderModel = await OrderService(db_session=self.session).get(pk=self.pk)
        _check_status_wait_core(obj_db=obj_db)
        _check_price(origin_price=obj_db.price, client_price=self.schema.price)
        return obj_db
