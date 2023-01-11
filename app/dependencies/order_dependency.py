from fastapi import Depends, HTTPException, status
from services.service_service import ServiceNameService

from services.client_service import ClientService

from models.order_model import OrderInSchema
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_session
from services.employee_service import EmployeeService


async def valid_post_schema(schema: OrderInSchema, session: AsyncSession = Depends(get_session)) -> OrderInSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
    mapper = {'employee_id': EmployeeService, 'client_id': ClientService, 'service_id': ServiceNameService}
    for field, class_service in mapper.items():
        pk = getattr(schema, field)
        service_helper = class_service(db_session=session)
        obj_db = await service_helper.get(pk=pk)
        if not obj_db:
            message = f'item with id {service_helper.name}.{pk} not found'
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return schema
