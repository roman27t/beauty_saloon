from typing import Optional

from pydantic import constr

from models.service_model import CategoryInSchema


class CategoryOptionalSchema(CategoryInSchema):
    name: Optional[constr(min_length=2, max_length=50)]
