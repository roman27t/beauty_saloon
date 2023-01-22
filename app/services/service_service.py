from typing import Type

from models import OfferLinkModel
from entities.service_name.service_model import ServiceNameModel
from services.base_service import AbstractService


class ServiceNameService(AbstractService):
    @property
    def _table(self) -> Type[ServiceNameModel]:
        return ServiceNameModel


class OfferLinkService(AbstractService):
    @property
    def _table(self) -> Type[OfferLinkModel]:
        return OfferLinkModel
