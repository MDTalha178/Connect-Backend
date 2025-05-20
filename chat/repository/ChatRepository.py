import datetime

from channels.db import database_sync_to_async
from django.db.models import QuerySet

from authentication.models import OnlineStatus
from chat.Services.ChatUserServices import ChatUserServices
from chat.models import ChatMessage
from common.Services.AsyncDataServices import AsyncDataAccessService


class ChatRepository(AsyncDataAccessService):

    def __init__(self):
        self.chat_user_service = ChatUserServices()
        super().__init__(ChatMessage)

    def filter(self, **kwargs) -> QuerySet:
        return self.model.objects.filter(**kwargs)

    @database_sync_to_async
    def update_read_status(self, receiver_id, sender_id, group_name):
        if self.chat_user_service.user_repo.get(id=receiver_id, online_status=OnlineStatus.ONLINE):
            self.filter(
                chat_config__chat_room_name=group_name, read_at__isnull=True
            ).exclude(sender_id=receiver_id).update(read_at=datetime.datetime.now())
