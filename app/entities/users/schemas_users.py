import datetime as dt
from typing import Optional

from pydantic import EmailStr, constr

from entities.users.models_user import _UserInSchema
from entities.users.choices_user import Gender


class EmployeeInSchema(_UserInSchema):
    ...


class ClientInSchema(_UserInSchema):
    ...


class _UserInOptionalSchema(_UserInSchema):
    phone: Optional[constr(min_length=10, max_length=14)]
    email: Optional[EmailStr]
    gender: Optional[Gender]
    last_name: Optional[constr(min_length=2, max_length=50)]
    first_name: Optional[constr(min_length=2, max_length=50)]
    birth_date: Optional[dt.date]


class EmployeeInOptionalSchema(_UserInOptionalSchema):
    ...


class ClientInOptionalSchema(_UserInOptionalSchema):
    ...
