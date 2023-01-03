from pydantic import constr, condecimal
from sqlalchemy import Column, VARCHAR
from sqlmodel import SQLModel, Field


class ServiceCategoryModel(SQLModel, table=True):
    __tablename__ = 'service_category'
    id: int = Field(default=None, primary_key=True)
    name: constr(min_length=2, max_length=50) = Field(sa_column=Column('name', VARCHAR, unique=True))
    detail: constr(max_length=50) = ''


# class ServiceTypeModel(SQLModel):
#     __tablename__ = 'service_type'
#     id: int = Field(default=None, primary_key=True)
#     name: constr(min_length=2, max_length=50) = Field(sa_column=Column('name', VARCHAR, unique=True))
#     detail: constr(max_length=50) = ''
#     price: condecimal(max_digits=5, decimal_places=2)
