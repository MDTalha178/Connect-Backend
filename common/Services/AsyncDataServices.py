from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from common.Interface.DataObjectLayer import DataObjectLayerInterface


class AsyncDataAccessService(DataObjectLayerInterface):
    def __init__(self, model):
        self.model = model

    @database_sync_to_async
    def create(self, **kwargs):
        instance = self.model.objects.create(**kwargs)
        return instance

    @database_sync_to_async
    def get(self, **kwargs):
        try:
            return self.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def filter(self, **kwargs) -> QuerySet:
        return self.model.objects.filter(**kwargs)

    @database_sync_to_async
    def update(self, instance, **kwargs):
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @database_sync_to_async
    def delete(self, instance):
        instance.delete()
