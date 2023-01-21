from typing import Type

from models.base_models import BaseSQLModel
from services.base_service import AbstractService


class ServiceRegistry:
    REGISTRY = {}
    @classmethod
    def register(cls, model: Type[BaseSQLModel], service_class: Type[AbstractService]):
        cls.REGISTRY[model.__table__.name] = service_class

    @classmethod
    def get(cls, model: Type[BaseSQLModel]) -> Type[AbstractService]:
        return cls.REGISTRY[model.__table__.name]
