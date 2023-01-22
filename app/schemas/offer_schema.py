from typing import Dict, List, Optional
from decimal import Decimal

from pydantic import Field, validator, condecimal

from entities.users.models_user import EmployeeModel, OfferLinkModel
from entities.service_name.models_service_name import ServiceNameModel
from models.offer_model import OfferLinkInSchema
from schemas.base_schema import BasePydanticSchema
from entities.category.schemas_category import CategoryInSchema


class OfferLinkOptionalSchema(OfferLinkInSchema):
    employee_id: Optional[int]
    service_name_id: Optional[int]
    rate: Optional[condecimal(max_digits=7, decimal_places=2)]


class _OfferFullSchema(OfferLinkInSchema):
    service: ServiceNameModel = Field(alias='service_name')
    price: Optional[condecimal(max_digits=7, decimal_places=2)] = None

    @validator('price', always=True)
    def set_price(cls, v: Optional[Decimal], values: dict) -> Decimal:
        return v or (Decimal(values['service'].price * values['rate'])).normalize()


class OfferFullResponseSchema(BasePydanticSchema):
    employee: EmployeeModel
    offers: List[_OfferFullSchema] = []
    categories: Dict[int, CategoryInSchema] = {}

    @classmethod
    def build(cls, offers: List[OfferLinkModel]) -> 'OfferFullResponseSchema':
        obj = cls(employee=offers[0].employee)
        for offer in offers:
            full_schema = _OfferFullSchema.from_orm(offer)
            if full_schema.service.category_id not in obj.categories:
                obj.categories[full_schema.service.category_id] = offer.service_name.category
            obj.offers.append(full_schema)
        return obj
