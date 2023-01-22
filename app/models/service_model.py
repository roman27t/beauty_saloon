from typing import TYPE_CHECKING, List, Union

from pydantic import constr, condecimal
from sqlmodel import Field, Relationship
from sqlalchemy import UniqueConstraint

from category.model_category import CategoryModel
from models.base_models import BaseSQLModel, DateCreatedChangedBase

if TYPE_CHECKING:
    from models import OrderModel, OfferLinkModel


class ServiceNameInSchema(BaseSQLModel):
    category_id: int = Field(foreign_key='category.id')
    name: constr(min_length=2, max_length=100)
    is_active: Union[bool, None] = True
    price: condecimal(max_digits=7, decimal_places=2)
    detail: constr(max_length=50) = ''


class ServiceNameModel(DateCreatedChangedBase, ServiceNameInSchema, table=True):
    __tablename__ = 'service_name'
    id: int = Field(default=None, primary_key=True)

    category: CategoryModel = Relationship(back_populates='services')
    # employees: List['EmployeeModel'] = Relationship(back_populates="services_name", link_model=OfferLinkModel)
    employee_links: List['OfferLinkModel'] = Relationship(back_populates="service_name")
    orders: List['OrderModel'] = Relationship(back_populates='service')

    __table_args__ = (UniqueConstraint('name', 'category_id', name='service_name_unique'),)
