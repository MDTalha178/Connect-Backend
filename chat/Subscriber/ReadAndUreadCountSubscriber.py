from chat.Services.ChatServices import ChatServices
from common.interface import SubscriberInterface, PublisherInterface


class ReadAndUnreadSubscriber(SubscriberInterface):

    def __init__(self, channel_layer, group_name, room_id):
        self.channel_layer = channel_layer
        self.group_name = group_name
        self.chat_service = ChatServices()

        self.room_id = room_id

    async def update_subscriber(self, publisher: PublisherInterface, event):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'data': {**event}
            },
        )

        # update read and unread count into databases
        await self.chat_service.update_read_un_read_count(
            self.room_id, event['sender_id'], event['receiver_id']
        )

