import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.Dispatcher.EventDispatcher import EventDispatcher
from chat.Publisher.ChatPublisher import ChatPublisher
from chat.Subscriber.ChatSubscriber import ChatSubscriber
from chat.Subscriber.ReadAndUreadCountSubscriber import ReadAndUnreadSubscriber
from common.factory import MessageFactory
from common.interface import PublisherInterface, SubscriberInterface


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None

        # here we define our publisher
        self.chat_publisher: PublisherInterface = ChatPublisher()

        # Here we define our factory
        self.factory = MessageFactory()

        # event dispatcher
        self.event_dispatcher = None

    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']

        # dispatch Event
        self.event_dispatcher = EventDispatcher(self.channel_layer, self.room_group_name)
        await self.event_dispatcher.channel_event_dispatch(channel_name=self.channel_name)

        # create  subscriber
        subscriber: SubscriberInterface = ChatSubscriber(self.channel_layer, self.room_group_name)
        self.chat_publisher.subscribe(subscriber)

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data: dict = json.loads(text_data)

        # Now subscribe for Read and unread count sent
        read_and_unread_subscriber: SubscriberInterface = ReadAndUnreadSubscriber(
            self.channel_layer, f'user_{text_data['receiver_id']}',
            self.room_group_name
        )

        # publish the read and unread count
        self.chat_publisher.subscribe(read_and_unread_subscriber)

        # Notify the subscriber there is some new update or new chat
        chat_message: dict = self.factory.create_chat_message(text_data, self.room_group_name)
        await self.chat_publisher.notify(chat_message)

        # Temporary unsubscribe
        self.chat_publisher.unsubscribe(read_and_unread_subscriber)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
