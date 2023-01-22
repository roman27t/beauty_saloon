from typing import Type

from models import OfferLinkModel
from services.base_service import AbstractService


class OfferLinkService(AbstractService):
    @property
    def _table(self) -> Type[OfferLinkModel]:
        return OfferLinkModel
