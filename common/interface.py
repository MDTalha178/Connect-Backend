from abc import ABC, abstractmethod
from typing import List


class GenerateInterface(ABC):

    @abstractmethod
    def generate(self, length=6):
        raise NotImplementedError("Sub class should have to implement this")


class VerificationInterface(ABC):

    @abstractmethod
    def verification(self, data: dict) -> bool:
        raise NotImplementedError("Sub class should have to implement this")


class SubscriberInterface(ABC):
    @abstractmethod
    async def update_subscriber(self, publisher: 'PublisherInterface', event):
        raise NotImplementedError("Sub class should have to implement this")


class PublisherInterface(ABC):
    subscriber: List[SubscriberInterface]

    @abstractmethod
    def subscribe(self, subscriber: SubscriberInterface):
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def unsubscribe(self, subscriber: SubscriberInterface):
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    async def notify(self, event):
        raise NotImplementedError("Sub class should have to implement this")


class EventDispatcherInterface(ABC):

    @abstractmethod
    def get_event_dispatch(self, **kwargs):
        raise NotImplementedError("Sub class should have to implement this")
