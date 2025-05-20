import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from authentication.models import User, OnlineStatus
from chat.models import ChatConfig, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.chat_config = None

    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        self.chat_config = await self.get_chat_config(self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        message = data['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id
            }
        )
        await self.save_message(data)
        await self.update_read_count(sender_id, receiver_id)

        # Send to receiver's global socket for unread counter
        await self.channel_layer.group_send(
            f'user_{receiver_id}',
            {
                'type': 'chat_message',
                'data': {
                    'message': message,
                    'sender_id': sender_id,
                    'receiver_id': receiver_id,
                    'room_name': f'user_{receiver_id}',
                    'config_id': str(self.chat_config.id)
                },
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
            'type': 'message',
            'room_name': self.room_group_name,
            'config_id': str(self.chat_config.id)
        }))

    @database_sync_to_async
    def get_chat_config(self, room_name):
        chat_config = ChatConfig.objects.filter(
            chat_room_name=str(self.room_group_name)).first()
        if chat_config:
            return chat_config
        return None

    @database_sync_to_async
    def save_message(self, data):
        ChatMessage.objects.create(
            messages=data['message'],
            chat_config_id=self.chat_config.id,
            sender_id=data['sender_id']
        )

    @database_sync_to_async
    def update_read_count(self, sender_id, receiver_id):
        if User.objects.filter(id=receiver_id, online_status=OnlineStatus.ONLINE).exists():
            ChatMessage.objects.filter(
                chat_config__chat_room_name=self.room_group_name,
                read_at__isnull=True
            ).exclude(
                sender_id=sender_id
            ).update(read_at=datetime.datetime.now())

        return None


class UserConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_group_name = None
        self.user_id = None
        self.global_group = 'global'

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'user_{str(self.user_id)}'

        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_add(self.global_group, self.channel_name)

        await self.channel_layer.group_send(
            self.global_group,
            {
                'type': 'chat_message',
                'data': {
                    'message_type': 'user_status',
                    'message': "User Online",
                    'user_id': self.user_id,
                    'status': 'Online'
                }
            }
        )

        await self.make_user_online()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.global_group,
            {
                'type': 'user_online',
                'data': {
                    'message_type': 'user_status',
                    'message': "User Offline",
                    'user_id': self.user_id,
                    'status': 'offline'
                }
            }
        )
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)
        await self.make_user_offline()

    async def user_online(self, event):
        await self.send(text_data=json.dumps(event['data']))
        await self.make_user_online()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def make_user_online(self):
        User.objects.filter(id=self.user_id).update(
            online_status=OnlineStatus.ONLINE
        )

    @database_sync_to_async
    def make_user_offline(self):
        User.objects.filter(id=self.user_id).update(
            online_status=OnlineStatus.OFFLINE
        )
