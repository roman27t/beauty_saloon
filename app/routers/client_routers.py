from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.client_dependency import valid_patch_id, valid_patch_schema
from models import ClientModel
from core.exceptions import DuplicatedEntryError
from models.database import get_session
from schemas.user_schemas import ClientInSchema, ClientInOptionalSchema
from services.client_service import ClientService

router_client = APIRouter()
ROUTE_CLIENT = '/client/'

#todo common class


@router_client.get(ROUTE_CLIENT + '{pk}/', response_model=ClientModel)
async def view_get_client_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    user = await ClientService(db_session=session).get(pk=pk)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return user


@router_client.get(ROUTE_CLIENT, response_model=list[ClientModel])
async def view_get_client_all(session: AsyncSession = Depends(get_session)):
    return await ClientService(db_session=session).get_all()


@router_client.post(ROUTE_CLIENT, response_model=ClientModel)
async def view_add_client(client: ClientInSchema, session: AsyncSession = Depends(get_session)):
    user_schema = ClientService(db_session=session).add(schema=client)
    try:
        await session.commit()
        return user_schema
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError('The client is already stored')


@router_client.patch(ROUTE_CLIENT + '{pk}/', response_model=ClientModel)
async def view_patch_client(
    schema: ClientInOptionalSchema=Depends(valid_patch_schema),
    employee_db: ClientModel=Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    ClientService(db_session=session).update(employee_db=employee_db, schema=schema)
    await session.commit()
    await session.refresh(employee_db)
    return employee_db
