from typing import Type

from models import CategoryModel, OfferLinkModel, ServiceNameModel
from services import ServiceRegistry
from services.base_service import AbstractService


class CategoryService(AbstractService):
    @property
    def _table(self) -> Type[CategoryModel]:
        return CategoryModel


class ServiceNameService(AbstractService):
    @property
    def _table(self) -> Type[ServiceNameModel]:
        return ServiceNameModel


class OfferLinkService(AbstractService):
    @property
    def _table(self) -> Type[OfferLinkModel]:
        return OfferLinkModel


ServiceRegistry.register(model=CategoryModel, service_class=CategoryService)
ServiceRegistry.register(model=CategoryModel, service_class=CategoryService)
ServiceRegistry.register(model=OfferLinkModel, service_class=OfferLinkService)
