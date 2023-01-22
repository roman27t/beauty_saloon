from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models import OrderModel
from entities.service_name.models_service_name import ServiceNameModel
from models.choices import StatusOrder
from routers.consts import RouteSlug
from models.database import get_session
from routers.choices import OrderFilter
from schemas.order_schema import (
    OrderPaymentSchema,
    OrderOptionalSchema,
    OrderFullResponseSchema,
)
from core.utils.pagination import Pagination
from schemas.payment_schema import PaymentContentSchema
from services.order_service import OrderService
from dependencies.order_dependency import (
    ValidPostOrderDependency,
    ValidPaymentOrderDependency,
    valid_status_wait,
)
from core.payment.api_pay.interface import ApiPay

router_order = APIRouter()
R_ORDER = '/order/'
ORDER_PAGE_SIZE = 5


@router_order.get(R_ORDER + RouteSlug.ifilter + RouteSlug.pk, response_model=list[OrderModel])
async def view_filter_order(ifilter: OrderFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    orders = await OrderService(db_session=session).filter(params)
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return orders


@router_order.get(R_ORDER + RouteSlug.full + RouteSlug.ifilter + RouteSlug.pk, response_model=OrderFullResponseSchema)
async def view_filter_order_full(
    ifilter: OrderFilter, pk: PositiveInt, session: AsyncSession = Depends(get_session), page: PositiveInt = 1
):
    params = {f'{ifilter.value}_id': pk}
    joins = [
        joinedload(getattr(OrderModel, ifilter.value)),
        selectinload(getattr(OrderModel, ifilter.invert())),
        selectinload(OrderModel.service).joinedload(ServiceNameModel.category),
    ]
    pagination = Pagination(page=page, page_size=ORDER_PAGE_SIZE)
    max_rows = await OrderService(db_session=session).count(params=params)
    pagination.check_set_max_page(page=page, max_rows=max_rows)
    orders = await OrderService(db_session=session).filter(params=params, options=joins, **pagination.to_dict())
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return OrderFullResponseSchema.build(orders=orders, source=ifilter, pagination=pagination)


@router_order.post(R_ORDER, response_model=OrderModel)
async def view_add_order(
    dependency: ValidPostOrderDependency = Depends(ValidPostOrderDependency),
    session: AsyncSession = Depends(get_session),
):
    schema = await dependency()
    return await OrderService(db_session=session).add(schema=schema)


@router_order.delete(R_ORDER + RouteSlug.pk, response_model=OrderModel)
async def view_delete_order(
    obj_db: OrderModel = Depends(valid_status_wait),
    session: AsyncSession = Depends(get_session),
):
    schema = OrderOptionalSchema(status=StatusOrder.CANCEL)
    await OrderService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db


@router_order.post(R_ORDER + 'payment/' + RouteSlug.pk, response_model=OrderModel)
async def view_order_payment(
    schema: OrderPaymentSchema,
    dependency: ValidPaymentOrderDependency = Depends(ValidPaymentOrderDependency),
    session: AsyncSession = Depends(get_session),
):
    obj_db = await dependency()
    content_payment = PaymentContentSchema(purpose=f'payment for order {obj_db.id}', price=obj_db.price)
    payment = ApiPay(card=schema.item, content=content_payment).pay()
    if not payment.status:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=payment.message)
    schema_update = OrderOptionalSchema(status=StatusOrder.PAID)
    await OrderService(db_session=session).update(obj_db=obj_db, schema=schema_update)
    return obj_db
