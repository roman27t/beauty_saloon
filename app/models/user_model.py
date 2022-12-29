import datetime as dt
# from enum import Enum
import enum
from typing import Union

from pydantic import EmailStr, constr
from sqlmodel import Field, Column, VARCHAR
from sqlalchemy import (Column, Integer, String)
from sqlalchemy_utils import ChoiceType
from sqlmodel import SQLModel, Field, Enum
from sqlalchemy.sql.sqltypes import Enum as EnumSQL
from models.base_models import DateCreatedChangedBase


class Gender(str, enum.Enum):
   MALE = 'M'
   FEMALE = 'F'


class UserBase(DateCreatedChangedBase):
    id: int = Field(default=None, primary_key=True)
    phone: constr(min_length=10, max_length=14) = Field(sa_column=Column('phone', VARCHAR, unique=True, index=True))
    email: EmailStr
    # gender: Gender = Field(sa_column=Column(ChoiceType(Gender, impl=String()), nullable=False), max_length=1)
    # gender: Gender = Field(sa_column=Column(Enum(Gender, values_callable=lambda enum: [e.value for e in enum])), nullable=False, max_length=1)
    # gender: Gender = Field(default=Gender.MALE, sa_column=Column(EnumSQL(Gender), nullable=False))
    last_name: constr(min_length=2, max_length=50)
    first_name: constr(min_length=2, max_length=50)
    birth_date: dt.date
    is_active: Union[bool, None] = True


class EmployeeModel(UserBase, table=True):
    __tablename__ = 'employee'


class ClientModel(UserBase, table=True):
    __tablename__ = 'client'


# class CityModel(CitySchema, table=True):
#     id: int = Field(default=None, primary_key=True)
    # __table_args__ = (
    #     Index(
    #         "compound_index_origin_name_version_destination_name", "origin_name", "origin_version", "destination_name"
    #     ),
    # )

# User [Client, Master] (email)
#-------------
# + email
# + phone
# + first_name
# + last_name
# + birthday
# + is_active: Union[bool, None] = True

# Service (type_service, name)
#-------------
# name
# amount
# description
# type_service ?

#Master-Service
# Master
# Service


# Order
#------
# Client
# Master
# Log_Order
# is_active
# date_start
# date_end

# Log_Order
# -------------
# amount
# description   [Service]
# comment
# name
# type_service

# Notification
# ---------------
# Order
# type_notification


