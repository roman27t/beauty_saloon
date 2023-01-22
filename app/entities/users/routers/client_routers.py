from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import ValidGetByIdDependency, valid_empty_schema
from routers.consts import RouteSlug
from models.database import get_session
from entities.users.models_user import ClientModel
from entities.users.schemas_users import ClientInSchema, ClientInOptionalSchema
from entities.users.services.client_service import ClientService

router_client = APIRouter()
ROUTE_CLIENT = '/client/'


@router_client.get(ROUTE_CLIENT + RouteSlug.pk, response_model=ClientModel)
async def view_get_client_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    return await ClientService(db_session=session).get(pk=pk)


@router_client.get(ROUTE_CLIENT, response_model=list[ClientModel])
async def view_get_client_all(session: AsyncSession = Depends(get_session)):
    return await ClientService(db_session=session).get_all()


@router_client.post(ROUTE_CLIENT, response_model=ClientModel)
async def view_add_client(client: ClientInSchema, session: AsyncSession = Depends(get_session)):
    return await ClientService(db_session=session).add(schema=client)


@router_client.patch(ROUTE_CLIENT + RouteSlug.pk, response_model=ClientModel)
async def view_patch_client(
    schema: ClientInOptionalSchema = Depends(valid_empty_schema(class_schema=ClientInOptionalSchema)),
    employee_db: ClientModel = Depends(ValidGetByIdDependency(class_service=ClientService)),
    session: AsyncSession = Depends(get_session),
):
    await ClientService(db_session=session).update(obj_db=employee_db, schema=schema)
    return employee_db
