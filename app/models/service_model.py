from typing import List, Union

from pydantic import constr, condecimal
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import VARCHAR, Column, UniqueConstraint


class ServiceCategoryModel(SQLModel, table=True):
    __tablename__ = 'service_category'
    id: int = Field(default=None, primary_key=True)
    name: constr(min_length=2, max_length=50) = Field(sa_column=Column('name', VARCHAR, unique=True))
    is_active: Union[bool, None] = True
    detail: constr(max_length=50) = ''

    services: List['ServiceNameModel'] = Relationship(back_populates='category')


class ServiceNameModel(SQLModel, table=True):
    __tablename__ = 'service_name'
    id: int = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key='service_category.id')
    name: constr(min_length=2, max_length=100)
    is_active: Union[bool, None] = True
    price: condecimal(max_digits=5, decimal_places=2)
    detail: constr(max_length=50) = ''

    category: ServiceCategoryModel = Relationship(back_populates='services')

    __table_args__ = (UniqueConstraint('name', 'category_id', name='service_name_unique'),)
