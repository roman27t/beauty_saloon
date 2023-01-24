from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks, status
from pydantic import PositiveInt
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backgrounds import task_clear_db_cache
from routers.consts import RouteSlug
from models.database import get_session
from core.utils.decorators import cached
from core.utils.pagination import Pagination
from core.utils.time_seconds import TimeSeconds
from entities.order.models_order import OrderModel
from entities.order.choices_order import OrderFilter, StatusOrder
from entities.order.services_order import OrderService
from entities.order.dependencies_order import (
    ValidPostOrderDependency,
    ValidPaymentOrderDependency,
    valid_status_wait,
)
from entities.order.schemas.schema_order import (
    OrderPaymentSchema,
    OrderOptionalSchema,
    OrderFullResponseSchema,
)
from entities.order.schemas.schema_payment import PaymentContentSchema
from entities.service_name.models_service_name import ServiceNameModel
from core.webservices.payment.api_pay.interface import ApiPay

router_order = APIRouter()
R_ORDER = '/order/'
ORDER_PAGE_SIZE = 5


@router_order.get(R_ORDER + RouteSlug.ifilter + RouteSlug.pk, response_model=list[OrderModel])
@cached(expire=TimeSeconds.M5, extra_keys=['pk', 'ifilter'])
async def view_filter_order(ifilter: OrderFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {ifilter.get_value_id: pk}
    orders = await OrderService(db_session=session).filter(params)
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return orders


@router_order.get(R_ORDER + RouteSlug.full + RouteSlug.ifilter + RouteSlug.pk, response_model=OrderFullResponseSchema)
@cached(expire=TimeSeconds.M5, extra_keys=['pk', 'ifilter', 'page'])
async def view_filter_order_full(
    ifilter: OrderFilter, pk: PositiveInt, session: AsyncSession = Depends(get_session), page: PositiveInt = 1
):
    params = {ifilter.get_value_id: pk}
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
    background_tasks: BackgroundTasks,
    dependency: ValidPostOrderDependency = Depends(ValidPostOrderDependency),
    session: AsyncSession = Depends(get_session),
):
    schema = await dependency()
    result = await OrderService(db_session=session).add(schema=schema)
    background_tasks.add_task(task_clear_db_cache)
    return result


@router_order.delete(R_ORDER + RouteSlug.pk, response_model=OrderModel)
async def view_delete_order(
    background_tasks: BackgroundTasks,
    obj_db: OrderModel = Depends(valid_status_wait),
    session: AsyncSession = Depends(get_session),
):
    schema = OrderOptionalSchema(status=StatusOrder.CANCEL)
    await OrderService(db_session=session).update(obj_db=obj_db, schema=schema)
    background_tasks.add_task(task_clear_db_cache)
    return obj_db


@router_order.post(R_ORDER + 'payment/' + RouteSlug.pk, response_model=OrderModel)
async def view_order_payment(
    background_tasks: BackgroundTasks,
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
    background_tasks.add_task(task_clear_db_cache)
    return obj_db


@router_order.get(RouteSlug.stats + R_ORDER  + RouteSlug.ifilter, response_model=dict)
async def view_order_statistic(ifilter: OrderFilter, session: AsyncSession = Depends(get_session), min_price: int = 1):
    field_select = getattr(OrderModel, ifilter.get_value_id)
    field_invert = getattr(OrderModel, ifilter.get_value_invert_id)
    total_price = func.sum(OrderModel.price).label('total_price')
    query = select(
        total_price,
        func.count(field_invert).label('total_user'),
        field_select,
    ).where(OrderModel.status==StatusOrder.WAIT).group_by(field_select).having(total_price > min_price)
    result = await session.execute(query)
    orders = result.all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id not found')
    return {'orders': orders}
