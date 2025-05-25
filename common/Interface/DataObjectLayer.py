from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from django.db.models import QuerySet, Model

T = TypeVar('T', bound=Model)


class DataObjectLayerInterface(Generic[T], ABC):

    @abstractmethod
    def filter(self, **filters) -> QuerySet[T]:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def get(self, **filters) -> T:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def create(self, data: dict) -> bool:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def update(self, instance, **kwargs) -> bool:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def delete(self, id: str) -> bool:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def idempotent_update(self, idempotent, **kwargs):
        raise NotImplementedError("Sub class should have to implement this")
