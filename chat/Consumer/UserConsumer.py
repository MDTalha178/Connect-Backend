import json
from channels.generic.websocket import AsyncWebsocketConsumer
from authentication.models import OnlineStatus
from chat.Consumer.GlobalConsumer import GlobalConsumer
from chat.Dispatcher.EventDispatcher import EventDispatcher
from chat.Publisher.ChatPublisher import ChatPublisher
from chat.Publisher.GlobalPublisher import GlobalPublisher
from common.factory import MessageFactory
from common.interface import PublisherInterface


class UserConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None

        # User_id
        self.user_id = None

        # Global Room Name
        self.global_consumer = None

        # here we define our publisher
        self.chat_publisher: PublisherInterface = ChatPublisher()

        # here we define our global publisher
        self.global_publisher: PublisherInterface = GlobalPublisher()

        # Here we define our factory
        self.factory = MessageFactory()

        # event dispatcher
        self.event_dispatcher = None

        # global event dispatcher
        self.global_event_dispatcher = None

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'user_{str(self.user_id)}'

        # dispatch Event for user
        self.event_dispatcher = EventDispatcher(self.channel_layer, self.room_group_name)
        await self.event_dispatcher.channel_event_dispatch(channel_name=self.channel_name)

        # Create a global consumer
        self.global_consumer = GlobalConsumer(self.channel_layer)

        # dispatch a global consumer
        await self.global_consumer.global_event_dispatcher(channel_name=self.channel_name)

        # here  we need to immediately publish user status
        await self.global_consumer.publish_user_status(user_id=self.user_id, status=OnlineStatus.ONLINE)

        await self.accept()

    async def disconnect(self, code):
        # before closing connection we need to publish the user status
        await self.global_consumer.publish_user_status(self.user_id, OnlineStatus.OFFLINE)

        # Closing websocket connection
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def chat_message(self, event):
        print("Called")
        print(event)
        await self.send(text_data=json.dumps(event))
