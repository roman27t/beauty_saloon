import datetime as dt
from typing import TYPE_CHECKING, Union
from decimal import Decimal

from pydantic import condecimal, constr
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Enum as EnumSQL

from models.base_models import DateCreatedChangedBase
from models.choices import StatusOrder

if TYPE_CHECKING:
    from models import EmployeeModel, ClientModel, ServiceNameModel


class OrderInSchema(SQLModel):
    employee_id: int = Field(foreign_key='employee.id')
    client_id: int = Field(foreign_key='client.id', index=True)
    # service_name_id: int = Field(foreign_key='service_name.id', index=True)
    start_at: dt.datetime
    end_at: dt.datetime
    comment: constr(max_length=255) = ''


class OrderModel(DateCreatedChangedBase, OrderInSchema, table=True):
    __tablename__ = 'order'

    id: int = Field(default=None, primary_key=True)
    expired_at: dt.datetime
    status: StatusOrder = Field(
        sa_column=Column(EnumSQL(StatusOrder), nullable=False, default=StatusOrder.WAIT.value), max_length=1
    )

    employee: 'EmployeeModel' = Relationship(back_populates='client_orders')
    client: 'ClientModel' = Relationship(back_populates='employee_orders')
    order_detail: 'OrderDetailModel' = Relationship(
        sa_relationship_kwargs={'uselist': False} , back_populates='order'
    )
    # service_order: 'ServiceNameModel' = Relationship(back_populates='orders')

    __table_args__ = (UniqueConstraint('employee_id', 'start_at', 'end_at', name='order_unique'),)


class OrderDetailModel(DateCreatedChangedBase, table=True):
    __tablename__ = 'order_detail'

    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key='order.id', unique=True)
    price: condecimal(max_digits=7, decimal_places=2)
    category: constr(min_length=2, max_length=50)
    name: constr(min_length=2, max_length=100)
    detail: constr(max_length=50) = ''

    order: 'OrderModel' = Relationship(back_populates='order_detail')
