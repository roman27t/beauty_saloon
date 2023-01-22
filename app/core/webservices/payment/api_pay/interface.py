from dataclasses import dataclass

from entities.order.schemas.schema_payment import (
    CardSchema,
    PaymentContentSchema,
    ResponsePaymentSchema,
)


@dataclass
class ApiPay:
    card: CardSchema
    content: PaymentContentSchema

    def pay(self) -> ResponsePaymentSchema:
        if self.card.cvv == '777':
            return ResponsePaymentSchema(status=True)
        return ResponsePaymentSchema(status=False, code='A1111', message='')
