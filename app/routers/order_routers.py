from enum import Enum
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import OrderModel
from models.choices import StatusOrder
from routers.consts import RouteSlug
from models.database import get_session
from models.order_model import OrderInSchema
from schemas.order_schema import OrderOptionalSchema
from services.order_service import OrderService
from dependencies.order_dependency import valid_patch_id, valid_post_schema

router_order = APIRouter()
ORDER_SERVICE = '/order/'


class OrderFilter(str, Enum):
    employee = 'employee'
    client = 'client'


@router_order.get(ORDER_SERVICE + RouteSlug.ifilter + RouteSlug.pk, response_model=list[OrderModel])
async def view_filter_order(ifilter: OrderFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    orders = await OrderService(db_session=session).filter(params)
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return orders


@router_order.post(ORDER_SERVICE, response_model=OrderModel)
async def view_add_order(
    schema: OrderInSchema = Depends(valid_post_schema), session: AsyncSession = Depends(get_session)
):
    return await OrderService(db_session=session).add(schema=schema)


@router_order.delete(ORDER_SERVICE + RouteSlug.pk, response_model=OrderModel)
async def view_delete_order(
    obj_db: OrderModel = Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    schema = OrderOptionalSchema(status=StatusOrder.CANCEL)
    await OrderService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db
