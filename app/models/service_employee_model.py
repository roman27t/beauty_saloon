from decimal import Decimal

from pydantic import condecimal
from sqlalchemy import UniqueConstraint


from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
if TYPE_CHECKING:
    from models import EmployeeModel, ServiceNameModel


class OfferLinkModel(SQLModel, table=True):
    __tablename__ = 'offer_link'

    id: int = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(
        foreign_key='employee.id',
    )
    service_name_id: Optional[int] = Field(
        foreign_key='service_name.id', index=True,
    )
    rate: condecimal(max_digits=3, decimal_places=2, ge=Decimal(1), le=Decimal(5)) = Decimal(1)

    employee: "EmployeeModel" = Relationship(back_populates="service_name_links")
    service_name: "ServiceNameModel" = Relationship(back_populates="employee_links")

    __table_args__ = (UniqueConstraint('service_name_id','employee_id', name='service_offer_unique'),)
