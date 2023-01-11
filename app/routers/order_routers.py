from enum import Enum

from fastapi import Depends, APIRouter, HTTPException, status
from services.order_service import OrderService

from models.order_model import OrderInSchema
from sqlalchemy.ext.asyncio import AsyncSession

from models import OrderModel
from routers.consts import RouteSlug
from models.database import get_session
# from dependencies.offer_dependency import valid_patch_id, valid_patch_schema

order_service = APIRouter()
ORDER_SERVICE = '/offer/'



@order_service.post(ORDER_SERVICE, response_model=OrderModel)
async def view_add_order(schema: OrderInSchema, session: AsyncSession = Depends(get_session)):
    return await OrderService(db_session=session).add(schema=schema)


# @order_service.patch(ORDER_SERVICE + RouteSlug.pk, response_model=OfferLinkModel)
# async def view_patch_offer(
#     schema: OfferLinkOptionalSchema = Depends(valid_patch_schema),
#     obj_db: OfferLinkModel = Depends(valid_patch_id),
#     session: AsyncSession = Depends(get_session),
# ):
#     await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
#     return obj_db
#
#
# @order_service.delete(ORDER_SERVICE + RouteSlug.pk, response_model=OfferLinkModel)
# async def view_delete_offer(
#     obj_db: OfferLinkModel = Depends(valid_patch_id),
#     session: AsyncSession = Depends(get_session),
# ):
#     schema = OfferLinkOptionalSchema(is_active=False)
#     await OfferLinkService(db_session=session).update(obj_db=obj_db, schema=schema)
#     return obj_db
