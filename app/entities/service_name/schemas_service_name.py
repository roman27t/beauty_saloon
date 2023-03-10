from typing import Optional

from pydantic import constr, condecimal

from entities.service_name.models_service_name import ServiceNameInSchema


class ServiceNameOptionalSchema(ServiceNameInSchema):
    category_id: Optional[int]
    name: Optional[constr(min_length=2, max_length=100)]
    price: Optional[condecimal(max_digits=7, decimal_places=2)]
