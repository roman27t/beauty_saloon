from typing import Union, List, TYPE_CHECKING

from pydantic import constr
from sqlalchemy import Column, VARCHAR
from sqlmodel import Field, Relationship

from models.base_models import BaseSQLModel, DateCreatedChangedBase
if TYPE_CHECKING:
    from entities.service_name.model_service_name import ServiceNameModel


class CategoryInSchema(BaseSQLModel):
    name: constr(min_length=2, max_length=50) = Field(sa_column=Column('name', VARCHAR, unique=True))
    is_active: Union[bool, None] = True
    detail: constr(max_length=50) = ''


class CategoryModel(DateCreatedChangedBase, CategoryInSchema, table=True):
    __tablename__ = 'category'
    id: int = Field(default=None, primary_key=True)

    services: List['ServiceNameModel'] = Relationship(back_populates='category')
