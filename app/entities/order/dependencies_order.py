import datetime as dt
from decimal import Decimal
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.order.models_order import OrderModel
from entities.offer.models_offer import OfferLinkModel
from entities.order.choices_order import StatusOrder
from models.database import get_session
from entities.order.models_order import OrderInSchema
from entities.order.schemas.schema_order import OrderPaymentSchema
from entities.order.services_order import OrderService
from entities.users.services.client_service import ClientService
from entities.offer.services_offer import OfferLinkService
from entities.service_name.services_service_name import ServiceNameService
from dependencies import ValidGetByIdDependency


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

    def __post_init__(self):
        self._mapper = {'client_id': ClientService, 'service_id': ServiceNameService}
        self._obj_result = dict.fromkeys(list(self._mapper.keys()), None)

    async def __call__(self) -> OrderInSchema:
        offer_db = await self.__check_get_offer_db()
        await self.__check_set_db_items()
        self.__check_price(offer_db=offer_db)
        return self.schema

    async def __check_get_offer_db(self) -> OfferLinkModel:
        if not self.schema.dict(exclude_unset=True):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
        params = {'service_name_id': self.schema.service_id, 'employee_id': self.schema.employee_id}
        return await OfferLinkService(db_session=self.session).get_by_filter(params=params)

    async def __check_set_db_items(self):
        for field, class_service in self._mapper.items():
            pk = getattr(self.schema, field)
            service_helper = class_service(db_session=self.session)
            self._obj_result[field] = await service_helper.get(pk=pk, e_message=f'{service_helper.name}.{pk} not found')

    def __check_price(self, offer_db: OfferLinkModel):
        origin_price = count_price(
            price=self._obj_result['service_id'].price,
            rate=offer_db.rate,
            start_at=self.schema.start_at,
            end_at=self.schema.end_at,
        )
        if origin_price != self.schema.price:
            message = f'price error {origin_price} != {self.schema.price}'
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)


def count_price(price: Decimal, rate: Decimal, start_at: dt.datetime, end_at: dt.datetime) -> Decimal:
    _price = price * rate
    _parts = Decimal((end_at - start_at).total_seconds() / 60 / 30)
    return (_price * _parts).normalize()


@dataclass
class ValidPaymentOrderDependency:
    pk: int
    schema: OrderPaymentSchema
    session: AsyncSession = Depends(get_session)

    async def __call__(self) -> OrderModel:
        obj_db: OrderModel = await OrderService(db_session=self.session).get(pk=self.pk)
        _check_status_wait_core(obj_db=obj_db)
        if obj_db.price != self.schema.price:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='bad price')
        return obj_db
