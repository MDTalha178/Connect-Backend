from abc import ABC, abstractmethod

from channels.db import database_sync_to_async


class AsyncDataObjectLayerInterface(ABC):

    @abstractmethod
    @database_sync_to_async
    async def filter(self, **filters) -> list:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    @database_sync_to_async
    def get(self, **filters) -> list:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    @database_sync_to_async
    def create(self, data: dict) -> bool:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    @database_sync_to_async
    def update(self, instance, **kwargs) -> bool:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    @database_sync_to_async
    def delete(self, id: str) -> bool:
        raise NotImplementedError("Sub class should have to implement this")
