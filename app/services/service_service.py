from typing import Type

from entities.offer.offer_model import OfferLinkModel
from services.base_service import AbstractService


class OfferLinkService(AbstractService):
    @property
    def _table(self) -> Type[OfferLinkModel]:
        return OfferLinkModel
