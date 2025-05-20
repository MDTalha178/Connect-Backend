from chat.Services.ChatUserServices import ChatUserServices
from common.interface import SubscriberInterface, PublisherInterface


class GlobalSubscriber(SubscriberInterface):

    def __init__(self, channel_layer, group_name="GLOBAL"):
        self.channel_layer = channel_layer
        self.group_name = group_name

        self.chat_user_service = ChatUserServices()

    async def update_subscriber(self, publisher: PublisherInterface, event):
        await self.channel_layer.group_send(
            self.group_name,
            {
                **event,
                'type': 'chat_message',
            },
        )

        # we need to update the user status
        await self.chat_user_service.set_user_status(event)
