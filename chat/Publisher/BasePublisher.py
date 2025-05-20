from typing import List
from common.interface import PublisherInterface, SubscriberInterface


class BasePublisher(PublisherInterface):
    subscriber_list = List[SubscriberInterface]

    def __init__(self, subscriber_list=None):
        if subscriber_list is None:
            subscriber_list = []
        self.subscriber_list = subscriber_list

    def subscribe(self, subscriber: SubscriberInterface):
        if subscriber not in self.subscriber_list:
            self.subscriber_list.append(subscriber)

    def unsubscribe(self, subscriber: SubscriberInterface):
        self.subscriber_list.remove(subscriber)

    async def notify(self, event):
        for subs in self.subscriber_list:
            await subs.update_subscriber(self, event)