from fastapi import Depends, APIRouter
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
