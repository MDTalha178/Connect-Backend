from chat.Dispatcher.EventDispatcher import EventDispatcher
from chat.Publisher.GlobalPublisher import GlobalPublisher
from chat.Subscriber.GlobalSubscriber import GlobalSubscriber
from common.factory import MessageFactory
from common.interface import PublisherInterface


class GlobalConsumer:

    def __init__(self, channel_layer, group_name="GLOBAL"):
        self.channel_layer = channel_layer
        self.group_name = group_name

        # event dispatcher
        self.event_dispatcher = EventDispatcher(self.channel_layer, self.group_name)

        # here we define our global publisher
        self.global_publisher: PublisherInterface = GlobalPublisher()

        # create global subscriber
        self.global_subscriber = GlobalSubscriber(self.channel_layer, self.group_name)

        # subscribe the global subscriber
        self.global_publisher.subscribe(self.global_subscriber)

        # Here we define our factory
        self.factory = MessageFactory()

    async def global_event_dispatcher(self, channel_name):
        await self.event_dispatcher.channel_event_dispatch(channel_name=channel_name)

    async def publish_user_status(self, user_id, status):

        # get a message format for user status
        user_status_massage: dict = self.factory.create_status_message(user_id, status)

        # Publish the user status
        await self.global_publisher.notify(user_status_massage)

