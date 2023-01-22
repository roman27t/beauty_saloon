from typing import TYPE_CHECKING, Union
from decimal import Decimal

from pydantic import condecimal
from sqlmodel import Field, Relationship
from sqlalchemy import UniqueConstraint

from models.base_models import BaseSQLModel, DateCreatedChangedBase

if TYPE_CHECKING:
    from entities.service_name.service_model import ServiceNameModel
    from entities.users.models_user import EmployeeModel


class OfferLinkInSchema(BaseSQLModel):
    employee_id: int = Field(foreign_key='employee.id')
    service_name_id: int = Field(foreign_key='service_name.id', index=True)
    rate: condecimal(max_digits=3, decimal_places=2, ge=Decimal(1), le=Decimal(5)) = Decimal(1)
    is_active: Union[bool, None] = True


class OfferLinkModel(DateCreatedChangedBase, OfferLinkInSchema, table=True):
    __tablename__ = 'offer_link'

    id: int = Field(default=None, primary_key=True)

    employee: 'EmployeeModel' = Relationship(back_populates='service_name_links')
    service_name: 'ServiceNameModel' = Relationship(back_populates='employee_links')

    __table_args__ = (UniqueConstraint('service_name_id', 'employee_id', name='service_offer_unique'),)
