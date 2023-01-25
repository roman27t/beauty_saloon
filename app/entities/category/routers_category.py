from fastapi import Depends, APIRouter, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from backgrounds import task_clear_cache, task_clear_db_cache
from dependencies import ValidGetByIdDependency, valid_empty_schema
from routers.consts import RouteSlug
from models.database import get_session
from core.utils.decorators import cached
from core.utils.time_seconds import TimeSeconds
from entities.category.models_category import CategoryModel
from entities.category.schemas_category import CategoryOptionalSchema
from entities.category.services_category import CategoryService

router_category = APIRouter()
ROUTE_CATEGORY = '/category/'


@router_category.get(ROUTE_CATEGORY + RouteSlug.pk, response_model=CategoryModel)
async def view_get_category_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    return await CategoryService(db_session=session).get(pk=pk)


@router_category.get(ROUTE_CATEGORY, response_model=list[CategoryModel])
@cached(expire=TimeSeconds.DAY)
async def view_get_category_all(session: AsyncSession = Depends(get_session)):
    return await CategoryService(db_session=session).get_all()


@router_category.post(ROUTE_CATEGORY, response_model=CategoryModel)
async def view_add_category(
    client: CategoryModel, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)
):
    result = await CategoryService(db_session=session).add(schema=client)
    background_tasks.add_task(task_clear_cache, keys=view_get_category_all.__name__)
    return result


@router_category.patch(ROUTE_CATEGORY + RouteSlug.pk, response_model=CategoryModel)
async def view_patch_category(
    background_tasks: BackgroundTasks,
    schema: CategoryOptionalSchema = Depends(valid_empty_schema(CategoryOptionalSchema)),
    obj_db: CategoryModel = Depends(ValidGetByIdDependency(class_service=CategoryService)),
    session: AsyncSession = Depends(get_session),
):
    await CategoryService(db_session=session).update(obj_db=obj_db, schema=schema)
    background_tasks.add_task(task_clear_db_cache)
    return obj_db
