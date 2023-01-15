from enum import Enum
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel, constr, condecimal
from pydantic.types import PaymentCardNumber


class PaymentType(str, Enum):
    CARD = 'card'


class CardSchema(PydanticBaseModel):
    number: PaymentCardNumber
    expire: constr(min_length=4, max_length=4)
    cvv: constr(min_length=3, max_length=3)


class PaymentContentSchema(PydanticBaseModel):
    purpose: constr(max_length=255)
    price: condecimal(max_digits=7, decimal_places=2)


class ResponsePaymentSchema(PydanticBaseModel):
    status: Optional[bool]
    code: str = ''
    message: str = ''
