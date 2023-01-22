from typing import TYPE_CHECKING, List, Union

from pydantic import constr
from sqlmodel import Field, Relationship
from sqlalchemy import VARCHAR, Column

from models.base_models import BaseSQLModel, DateCreatedChangedBase

if TYPE_CHECKING:
    from entities.service_name.models_service_name import ServiceNameModel


class CategoryInSchema(BaseSQLModel):
    name: constr(min_length=2, max_length=50) = Field(sa_column=Column('name', VARCHAR, unique=True))
    is_active: Union[bool, None] = True
    detail: constr(max_length=50) = ''


class CategoryModel(DateCreatedChangedBase, CategoryInSchema, table=True):
    __tablename__ = 'category'
    id: int = Field(default=None, primary_key=True)

    services: List['ServiceNameModel'] = Relationship(back_populates='category')
