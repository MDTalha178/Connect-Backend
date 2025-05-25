import datetime
from typing import List

from channels.db import database_sync_to_async

from chat.apps import ChatConfig
from chat.repository.ChatConfigurationRepository import ChatConfigurationRepository


class ChatConfigurationService:

    def __init__(self):
        self.chat_config_repo = ChatConfigurationRepository()

    def create_chat(self, **kwargs):
        return self.chat_config_repo.create_chat(**kwargs)

    @database_sync_to_async
    def update_chat_list(self, **kwargs):
        chat_config_instance = self.chat_config_repo.get(id=kwargs.get('config_id'))
        self.chat_config_repo.update(chat_config_instance, updated_at=datetime.datetime.now())

    def get_participant_list(self, chat_config: ChatConfig) -> List[str]:
        return self.chat_config_repo.get_participant_list(chat_config)
