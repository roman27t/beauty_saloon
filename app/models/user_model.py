import datetime as dt
from typing import Union

from pydantic import EmailStr, constr
from sqlmodel import VARCHAR, Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Enum as EnumSQL

from models.choices import Gender
from models.base_models import DateCreatedChangedBase


class _UserInSchema(SQLModel):
    phone: constr(min_length=10, max_length=14) = Field(sa_column=Column('phone', VARCHAR, unique=True, index=True))
    email: EmailStr
    gender: Gender = Field(sa_column=Column(EnumSQL(Gender), nullable=False), max_length=1)
    last_name: constr(min_length=2, max_length=50)
    first_name: constr(min_length=2, max_length=50)
    birth_date: dt.date


class _UserBase(DateCreatedChangedBase, _UserInSchema):
    id: int = Field(default=None, primary_key=True)
    is_active: Union[bool, None] = True


class EmployeeModel(_UserBase, table=True):
    __tablename__ = 'employee'


class ClientModel(_UserBase, table=True):
    __tablename__ = 'client'
