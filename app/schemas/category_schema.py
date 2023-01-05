from pydantic import constr
from typing import Optional
from models.service_model import CategoryInSchema


class CategoryOptionalSchema(CategoryInSchema):
    name: Optional[constr(min_length=2, max_length=50)]
