from typing import Type

from services.base_service import AbstractService
from entities.offer.models_offer import OfferLinkModel


class OfferLinkService(AbstractService):
    @property
    def _table(self) -> Type[OfferLinkModel]:
        return OfferLinkModel
