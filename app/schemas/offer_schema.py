from decimal import Decimal
from typing import Optional, List, Dict

from pydantic import condecimal, Field, validator

from models import ServiceNameModel, EmployeeModel, OfferLinkModel
from models.offer_model import OfferLinkInSchema
from models.service_model import CategoryInSchema
from schemas.base_schema import BasePydanticSchema


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
    def build(cls, data_db: List[OfferLinkModel]) -> 'OfferFullResponseSchema':
        obj = cls(employee=data_db[0].employee)
        for i in data_db:
            full_schema = _OfferFullSchema.from_orm(i)
            if full_schema.service.category_id not in obj.categories:
                obj.categories[full_schema.service.category_id] = i.service_name.category
            obj.offers.append(full_schema)
        return obj
