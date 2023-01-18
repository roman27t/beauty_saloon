from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import OrderModel, OfferLinkModel
from models.choices import StatusOrder
from models.database import get_session
from models.order_model import OrderInSchema
from services.order_service import OrderService
from services.client_service import ClientService
from services.service_service import OfferLinkService, ServiceNameService


async def valid_post_schema(schema: OrderInSchema, session: AsyncSession = Depends(get_session)) -> OrderInSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
    params = {'service_name_id': schema.service_id, 'employee_id': schema.employee_id}
    offer_db: OfferLinkModel = await OfferLinkService(db_session=session).get_by_filter(params=params)

    mapper = {'client_id': ClientService, 'service_id': ServiceNameService}
    obj_result = dict.fromkeys(list(mapper.keys()), None)
    for field, class_service in mapper.items():
        pk = getattr(schema, field)
        service_helper = class_service(db_session=session)
        obj_result[field] = await service_helper.get(pk=pk, e_message=f'item {service_helper.name}.{pk} not found')
    origin_price = offer_db.rate * obj_result['service_id'].price
    if origin_price != schema.price:
        message = f'price error {origin_price} != {schema.price}'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return schema


async def valid_patch_id(pk: int, session: AsyncSession = Depends(get_session)) -> OrderModel:
    return await OrderService(db_session=session).get(pk=pk)


async def valid_status_wait(obj_db: OrderModel = Depends(valid_patch_id)) -> OrderModel:
    if obj_db.status != StatusOrder.WAIT:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='status order already expired')
    return obj_db
