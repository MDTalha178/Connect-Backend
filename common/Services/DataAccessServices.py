from typing import Type, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Model

from common.Interface.DataObjectLayer import DataObjectLayerInterface

T = TypeVar('T', bound=Model)


class DataAccessService(DataObjectLayerInterface):
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, **kwargs) -> T:
        instance = self.model.objects.create(**kwargs)
        return instance

    def get(self, **kwargs) -> T:
        try:
            return self.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def filter(self, **kwargs) -> QuerySet[T]:
        return self.model.objects.filter(**kwargs)

    def update(self, instance, **kwargs) -> bool:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return True

    def delete(self, instance) -> bool:
        instance.delete()
        return True
