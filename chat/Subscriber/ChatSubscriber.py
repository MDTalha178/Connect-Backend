from chat.Services.ChatServices import ChatServices
from common.interface import SubscriberInterface, PublisherInterface


class ChatSubscriber(SubscriberInterface):

    def __init__(self, channel_layer, group_name):
        self.channel_layer = channel_layer
        self.group_name = group_name
        self.chat_service = ChatServices()

    async def update_subscriber(self, publisher: PublisherInterface, event: dict):
        await self.channel_layer.group_send(
            self.group_name,
            {
                **event,
                'type': 'chat_message',
             },
        )

        # save message into database
        await self.chat_service.save_chat(
            messages=event['message'], chat_config_id=event['config_id'],
            sender_id=event['sender_id']
        )
