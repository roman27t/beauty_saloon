from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict

from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import Field, condecimal, validator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import OfferLinkModel, EmployeeModel, ServiceNameModel
from models.service_model import CategoryInSchema
from routers.consts import RouteSlug
from models.database import get_session
from models.offer_model import OfferLinkInSchema
from routers.offer_routers import OfferFilter
from schemas.base_schema import BasePydanticSchema
from schemas.offer_schema import OfferLinkOptionalSchema
from services.service_service import OfferLinkService
from dependencies.offer_dependency import valid_patch_id, valid_patch_schema

router_offer_full = APIRouter()
OFFER_SERVICE = '/offer/full/'


from sqlalchemy import select


class OfferFullSchema(OfferLinkInSchema):
    service: ServiceNameModel = Field(alias='service_name')
    price: Optional[condecimal(max_digits=7, decimal_places=2)] = None

    @validator('price', always=True)
    def set_price(cls, v, values) -> Decimal:
        return Decimal(int(values['service'].price * values['rate']))


class OfferFullResponseSchema(BasePydanticSchema):
    employee: EmployeeModel
    offers: List[OfferFullSchema] = []
    categories: Dict[int, CategoryInSchema] = {}

    @classmethod
    def build(cls, data_db: List) -> 'OfferFullResponseSchema':
        obj = cls(employee=data_db[0].employee)
        for i in data_db:
            full_schema = OfferFullSchema.from_orm(i)
            if full_schema.service.category_id not in obj.categories:
                obj.categories[full_schema.service.category_id] = i.service_name.category
            obj.offers.append(full_schema)
        return obj


@router_offer_full.get(OFFER_SERVICE + RouteSlug.ifilter + RouteSlug.pk, response_model=OfferFullResponseSchema)
async def view_filter_offer_full(ifilter: OfferFilter, pk: int, session: AsyncSession = Depends(get_session)):
    params = {f'{ifilter.value}_id': pk}
    if ifilter.value == OfferFilter.service_name.value:
        params['is_active'] = True
    conditions = [getattr(OfferLinkModel, key) == value for key, value in params.items()]
    result = await session.execute(select(OfferLinkModel).where(*conditions).options(
        selectinload(OfferLinkModel.employee),
        selectinload(OfferLinkModel.service_name).selectinload(ServiceNameModel.category),
        )
    )
    data_db = result.scalars().all()
    if not data_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'item with id {pk} not found')
    return OfferFullResponseSchema.build(data_db=data_db)

