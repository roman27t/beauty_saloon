from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.decorators import cached
from dependencies import ValidGetByIdDependency, valid_empty_schema
from routers.consts import RouteSlug
from models.database import get_session
from entities.category.models_category import CategoryModel
from entities.category.schemas_category import CategoryOptionalSchema
from entities.category.services_category import CategoryService

router_category = APIRouter()
ROUTE_CATEGORY = '/category/'


@router_category.get(ROUTE_CATEGORY + RouteSlug.pk, response_model=CategoryModel)
async def view_get_category_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    return await CategoryService(db_session=session).get(pk=pk)


@router_category.get(ROUTE_CATEGORY, response_model=list[CategoryModel])
@cached(expire=60)
async def view_get_category_all(session: AsyncSession = Depends(get_session)):
    return await CategoryService(db_session=session).get_all()


@router_category.post(ROUTE_CATEGORY, response_model=CategoryModel)
async def view_add_category(client: CategoryModel, session: AsyncSession = Depends(get_session)):
    # todo remove cach background
    return await CategoryService(db_session=session).add(schema=client)


@router_category.patch(ROUTE_CATEGORY + RouteSlug.pk, response_model=CategoryModel)
async def view_patch_category(
    schema: CategoryOptionalSchema = Depends(valid_empty_schema(CategoryOptionalSchema)),
    obj_db: CategoryModel = Depends(ValidGetByIdDependency(class_service=CategoryService)),
    session: AsyncSession = Depends(get_session),
):
    await CategoryService(db_session=session).update(obj_db=obj_db, schema=schema)
    # todo remove cach background
    return obj_db
