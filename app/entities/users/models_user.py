import datetime as dt
from typing import TYPE_CHECKING, List, Union

from pydantic import EmailStr, constr
from sqlmodel import VARCHAR, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Enum as EnumSQL

from models.choices import Gender
from models.base_models import BaseSQLModel, DateCreatedChangedBase
from models.offer_model import OfferLinkModel

if TYPE_CHECKING:
    from models import OrderModel

_REGEX_NAME = '^[A-Za-z- ]+$'


class _UserInSchema(BaseSQLModel):
    phone: constr(min_length=10, max_length=14) = Field(sa_column=Column('phone', VARCHAR, unique=True, index=True))
    email: EmailStr
    gender: Gender = Field(sa_column=Column(EnumSQL(Gender), nullable=False), max_length=1)
    last_name: constr(regex=_REGEX_NAME, min_length=2, max_length=50, to_lower=True)
    first_name: constr(regex=_REGEX_NAME, min_length=2, max_length=50, to_lower=True)
    birth_date: dt.date


class _UserBase(DateCreatedChangedBase, _UserInSchema):
    id: int = Field(default=None, primary_key=True)
    is_active: Union[bool, None] = True


class EmployeeModel(_UserBase, table=True):
    __tablename__ = 'employee'

    # services_name: List['ServiceNameModel'] = Relationship(back_populates="employees", link_model=OfferLinkModel)
    service_name_links: List['OfferLinkModel'] = Relationship(back_populates="employee")
    client_orders: List['OrderModel'] = Relationship(back_populates="employee")


class ClientModel(_UserBase, table=True):
    __tablename__ = 'client'

    employee_orders: List['OrderModel'] = Relationship(back_populates="client")