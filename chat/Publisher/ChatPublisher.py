from typing import List

from chat.Publisher.BasePublisher import BasePublisher
from common.interface import SubscriberInterface


class ChatPublisher(BasePublisher):
    subscriber_list = List[SubscriberInterface]

    def __init__(self, subscriber_list=None):
        super().__init__(subscriber_list=subscriber_list)
