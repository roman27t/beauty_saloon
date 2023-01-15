from typing import Union

from pydantic import condecimal

from models.choices import StatusOrder
from schemas.base_schema import BasePydanticSchema
from schemas.payment_schema import PaymentType, CardSchema


class OrderOptionalSchema(BasePydanticSchema):
    status: StatusOrder


class OrderPaymentSchema(BasePydanticSchema):
    p_type: PaymentType
    item: Union[CardSchema]
    price: condecimal(max_digits=7, decimal_places=2)
