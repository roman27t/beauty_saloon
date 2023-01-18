import datetime as dt
from typing import TYPE_CHECKING

from pydantic import constr, validator, condecimal
from sqlmodel import Field, Relationship
from sqlalchemy import Column, UniqueConstraint
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql.sqltypes import Enum as EnumSQL

from models.choices import StatusOrder
from models.base_models import BaseSQLModel, DateCreatedChangedBase

if TYPE_CHECKING:
    from models import ClientModel, EmployeeModel, ServiceNameModel

MAX_PERIOD_IN_YEAR = 1
MAX_PERIOD_EVENT_HOUR = 4


class OrderInSchema(BaseSQLModel):
    employee_id: int = Field(foreign_key='employee.id')
    client_id: int = Field(foreign_key='client.id', index=True)
    service_id: int = Field(default=None, foreign_key='service_name.id')
    start_at: dt.datetime
    end_at: dt.datetime
    price: condecimal(max_digits=7, decimal_places=2)
    comment: constr(max_length=255) = ''

    @validator('start_at', 'end_at')
    def validate_dates(cls, v: dt.datetime) -> dt.datetime:
        v = v.replace(second=0, microsecond=0)
        if v.minute not in (0, 30):
            raise ValueError('time must be 1 hour or 30 minutes')
        date_today = dt.datetime.now()
        if date_today > v:
            raise ValueError('data in past')
        if v > date_today + relativedelta(years=MAX_PERIOD_IN_YEAR):
            raise ValueError(f'max period in {MAX_PERIOD_IN_YEAR} years - {v}')
        return v

    @validator('end_at')
    def validate_end_at(cls, v: dt.datetime, values: dict) -> dt.datetime:
        if values['start_at'] >= v:
            raise ValueError('end_at must be more start_at')
        if (v - values['start_at']) > dt.timedelta(hours=MAX_PERIOD_EVENT_HOUR):
            raise ValueError(f'max period {MAX_PERIOD_EVENT_HOUR} hours')
        return v


class OrderModel(DateCreatedChangedBase, OrderInSchema, table=True):
    __tablename__ = 'order'

    id: int = Field(default=None, primary_key=True)
    expired_at: dt.datetime
    status: StatusOrder = Field(
        sa_column=Column(EnumSQL(StatusOrder), nullable=False, default=StatusOrder.WAIT.value), max_length=2
    )

    employee: 'EmployeeModel' = Relationship(back_populates='client_orders')
    client: 'ClientModel' = Relationship(back_populates='employee_orders')
    order_detail: 'OrderDetailModel' = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates='order')
    service: 'ServiceNameModel' = Relationship(back_populates='orders')

    __table_args__ = (
        UniqueConstraint('employee_id', 'start_at', 'end_at', name='order_unique'),
        # Index('employee_id_start_at_end_at_index', 'employee_id', 'start_at', 'end_at', postgresql_using='gist'),
    )


class OrderDetailModel(DateCreatedChangedBase, table=True):
    __tablename__ = 'order_detail'

    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key='order.id', unique=True)
    category: constr(min_length=2, max_length=50)
    name: constr(min_length=2, max_length=100)
    detail: constr(max_length=50) = ''

    order: 'OrderModel' = Relationship(back_populates='order_detail')
