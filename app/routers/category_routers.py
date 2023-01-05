from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.category_dependency import valid_patch_schema, valid_patch_id
from models import CategoryModel
from models.database import get_session
from schemas.category_schema import CategoryOptionalSchema
from services.service_service import CategoryService

router_category = APIRouter()
ROUTE_CATEGORY = '/category/'


@router_category.get(ROUTE_CATEGORY + '{pk}/', response_model=CategoryModel)
async def view_get_category_by_id(pk: int, session: AsyncSession = Depends(get_session)):
    category = await CategoryService(db_session=session).get(pk=pk)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return category


@router_category.get(ROUTE_CATEGORY, response_model=list[CategoryModel])
async def view_get_category_all(session: AsyncSession = Depends(get_session)):
    return await CategoryService(db_session=session).get_all()


@router_category.post(ROUTE_CATEGORY, response_model=CategoryModel)
async def view_add_category(client: CategoryModel, session: AsyncSession = Depends(get_session)):
    return await CategoryService(db_session=session).add(schema=client)


@router_category.patch(ROUTE_CATEGORY + '{pk}/', response_model=CategoryModel)
async def view_patch_category(
    schema: CategoryOptionalSchema = Depends(valid_patch_schema),
    obj_db: CategoryModel = Depends(valid_patch_id),
    session: AsyncSession = Depends(get_session),
):
    await CategoryService(db_session=session).update(obj_db=obj_db, schema=schema)
    return obj_db
