from typing import TYPE_CHECKING, Union

from pydantic import constr, condecimal
from sqlmodel import Field, Relationship
from sqlalchemy import UniqueConstraint

from models.base_models import BaseSQLModel, DateCreatedChangedBase
from entities.category.models_category import CategoryModel

if TYPE_CHECKING:
    from entities.offer.models_offer import OfferModel
    from entities.order.models_order import OrderModel


class ServiceNameInSchema(BaseSQLModel):
    category_id: int = Field(foreign_key='category.id', index=True)
    name: constr(min_length=2, max_length=100)
    is_active: Union[bool, None] = True
    price: condecimal(max_digits=7, decimal_places=2)
    detail: constr(max_length=50) = ''


class ServiceNameModel(DateCreatedChangedBase, ServiceNameInSchema, table=True):
    __tablename__ = 'service_name'
    id: int = Field(default=None, primary_key=True)

    category: CategoryModel = Relationship(back_populates='services')
    employee_links: list['OfferModel'] = Relationship(back_populates='service_name')
    orders: list['OrderModel'] = Relationship(back_populates='service')

    __table_args__ = (UniqueConstraint('name', 'category_id', name='service_name_unique'),)
