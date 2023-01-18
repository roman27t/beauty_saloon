from enum import Enum

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import OrderModel
from models.choices import StatusOrder
from routers.consts import RouteSlug
from models.database import get_session
from schemas.order_schema import OrderPaymentSchema, OrderOptionalSchema
from schemas.payment_schema import PaymentContentSchema
from services.order_service import OrderService
from dependencies.order_dependency import ValidPostOrderDependency, valid_status_wait
from core.payment.api_pay.interface import ApiPay

router_order = APIRouter()
R_ORDER = '/order/'


class OrderFilter(str, Enum):
    employee = 'employee'
    client = 'client'


@router_order.get(R_ORDER + RouteSlug.ifilter + RouteSlug.pk, response_model=list[OrderModel])
async def view_filter_order(ifilter: OrderFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    orders = await OrderService(db_session=session).filter(params)
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return orders


@router_order.post(R_ORDER, response_model=OrderModel)
async def view_add_order(
        dependency: ValidPostOrderDependency = Depends(ValidPostOrderDependency),
        session: AsyncSession = Depends(get_session
    )
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
    obj_db: OrderModel = Depends(valid_status_wait),
    session: AsyncSession = Depends(get_session),
):
    content_payment = PaymentContentSchema(purpose=f'payment for order {obj_db.id}', price=obj_db.price)
    payment = ApiPay(card=schema.item, content=content_payment).pay()
    if not payment.status:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=payment.message)
    schema_update = OrderOptionalSchema(status=StatusOrder.PAID)
    await OrderService(db_session=session).update(obj_db=obj_db, schema=schema_update)
    return obj_db
