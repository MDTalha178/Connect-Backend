from chat.Publisher.BasePublisher import BasePublisher


class GlobalPublisher(BasePublisher):
    def __init__(self, subscriber_list=None):
        super().__init__(subscriber_list=subscriber_list)

