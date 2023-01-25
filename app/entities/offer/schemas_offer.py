from typing import Dict, List, Optional
from decimal import Decimal

from pydantic import validator, condecimal

from schemas import BasePydanticSchema
from entities.users.models_user import OfferModel, EmployeeModel
from entities.offer.models_offer import OfferInSchema
from entities.category.schemas_category import CategoryInSchema
from entities.service_name.models_service_name import ServiceNameModel


class OfferOptionalSchema(OfferInSchema):
    employee_id: Optional[int]
    service_name_id: Optional[int]
    rate: Optional[condecimal(max_digits=7, decimal_places=2)]


class _OfferFullSchema(OfferInSchema):
    service_name: ServiceNameModel
    price: Optional[condecimal(max_digits=7, decimal_places=2)] = None

    @validator('price', always=True)
    def set_price(cls, v: Optional[Decimal], values: dict) -> Decimal:
        return v or (Decimal(values['service_name'].price * values['rate'])).normalize()


class OfferFullResponseSchema(BasePydanticSchema):
    employee: EmployeeModel
    offers: List[_OfferFullSchema] = []
    categories: Dict[int, CategoryInSchema] = {}

    @classmethod
    def build(cls, offers: List[OfferModel]) -> 'OfferFullResponseSchema':
        obj = cls(employee=offers[0].employee)
        for offer in offers:
            full_schema = _OfferFullSchema.from_orm(offer)
            if full_schema.service_name.category_id not in obj.categories:
                obj.categories[full_schema.service_name.category_id] = offer.service_name.category
            obj.offers.append(full_schema)
        return obj
