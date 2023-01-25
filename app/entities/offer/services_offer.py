from typing import Type

from services.base_service import AbstractService
from entities.offer.models_offer import OfferModel


class OfferService(AbstractService):
    @property
    def _table(self) -> Type[OfferModel]:
        return OfferModel
