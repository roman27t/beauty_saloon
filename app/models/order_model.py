import datetime as dt
from typing import TYPE_CHECKING, Union
from decimal import Decimal

from pydantic import condecimal
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Enum as EnumSQL

from models.base_models import DateCreatedChangedBase
from models.choices import StatusOrder

if TYPE_CHECKING:
    from models import EmployeeModel, ClientModel


class OrderInSchema(SQLModel):
    employee_id: int = Field(foreign_key='employee.id')
    client_id: int = Field(foreign_key='client.id', index=True)
    start_at: dt.datetime
    end_at: dt.datetime


class OrderModel(DateCreatedChangedBase, OrderInSchema, table=True):
    __tablename__ = 'order'

    id: int = Field(default=None, primary_key=True)
    expired_at: dt.datetime
    status: StatusOrder = Field(
        sa_column=Column(EnumSQL(StatusOrder), nullable=False, default=StatusOrder.WAIT.value), max_length=1
    )

    employee: 'EmployeeModel' = Relationship(back_populates='client_orders')
    client: 'ClientModel' = Relationship(back_populates='employee_orders')

    __table_args__ = (UniqueConstraint('employee_id', 'start_at', 'end_at', name='order_unique'),)
