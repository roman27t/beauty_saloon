import datetime as dt
from typing import TYPE_CHECKING

from pydantic import constr, condecimal, validator
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.sql.sqltypes import Enum as EnumSQL

from models.choices import StatusOrder
from models.base_models import DateCreatedChangedBase

if TYPE_CHECKING:
    from models import ClientModel, EmployeeModel, ServiceNameModel

MAX_PERIOD = 300


class OrderInSchema(SQLModel):
    employee_id: int = Field(foreign_key='employee.id')
    client_id: int = Field(foreign_key='client.id', index=True)
    service_id: int = Field(default=None, foreign_key='service_name.id')
    start_at: dt.datetime
    end_at: dt.datetime
    price: condecimal(max_digits=7, decimal_places=2)
    comment: constr(max_length=255) = ''

    @validator('start_at', 'end_at')
    def validate_dates(cls, v: dt.datetime) -> dt.datetime:
        date_today = dt.datetime.now()
        if date_today > v:
            raise ValueError('data in past')
        if v > date_today + dt.timedelta(days=MAX_PERIOD):  # todo 1 year
            raise ValueError(f'max period {MAX_PERIOD} days - {v}')
        # todo кратное 30 минут
        return v

    @validator('end_at')
    def validate_end_at(cls, v: str, values) -> str:
        if values['start_at'] >= v:
            raise ValueError('end_at must be more start_at')
        return v


class OrderModel(DateCreatedChangedBase, OrderInSchema, table=True):
    __tablename__ = 'order'

    id: int = Field(default=None, primary_key=True)
    expired_at: dt.datetime
    status: StatusOrder = Field(
        sa_column=Column(EnumSQL(StatusOrder), nullable=False, default=StatusOrder.WAIT.value), max_length=1
    )

    employee: 'EmployeeModel' = Relationship(back_populates='client_orders')
    client: 'ClientModel' = Relationship(back_populates='employee_orders')
    order_detail: 'OrderDetailModel' = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates='order')
    service: 'ServiceNameModel' = Relationship(back_populates='orders')

    __table_args__ = (UniqueConstraint('employee_id', 'start_at', 'end_at', name='order_unique'),)


class OrderDetailModel(DateCreatedChangedBase, table=True):
    __tablename__ = 'order_detail'

    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key='order.id', unique=True)
    category: constr(min_length=2, max_length=50)
    name: constr(min_length=2, max_length=100)
    detail: constr(max_length=50) = ''

    order: 'OrderModel' = Relationship(back_populates='order_detail')
