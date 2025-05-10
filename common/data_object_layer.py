from abc import ABC, abstractmethod


class DataObjectLayerInterface(ABC):

    @abstractmethod
    def get_data(self, **filters) -> list:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def create(self, data: dict) -> bool:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def update(self, data: dict) -> bool:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def delete(self, id: str) -> bool:
        raise NotImplementedError("Sub class should have to implement this")
