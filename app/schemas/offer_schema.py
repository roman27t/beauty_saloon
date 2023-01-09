from typing import Optional

from pydantic import condecimal

from models.offer_model import OfferLinkInSchema


class OfferLinkOptionalSchema(OfferLinkInSchema):
    employee_id: Optional[int]
    service_name_id: Optional[int]
    rate: Optional[condecimal(max_digits=7, decimal_places=2)]
