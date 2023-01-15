from typing import Union

from pydantic import BaseModel as PydanticBaseModel, condecimal

from models.choices import StatusOrder
from schemas.payment_schema import PaymentType, CardSchema


class OrderOptionalSchema(PydanticBaseModel):
    status: StatusOrder


class OrderPaymentSchema(PydanticBaseModel):
    p_type: PaymentType
    item: Union[CardSchema]
    price: condecimal(max_digits=7, decimal_places=2)
