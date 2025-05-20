from chat.models import ChatConfig
from common.Generate import GenerateRoomId
from common.Services.DataAccessServices import DataAccessService


class ChatConfigurationRepository(DataAccessService):

    def __init__(self, *args, **kwargs):
        self.roomIdGeneration = GenerateRoomId()
        super().__init__(ChatConfig)

    def create_chat(self, **kwargs):
        participant_ids = kwargs.pop('participant_ids')
        chat_config_instance = self.create(chat_room_name=self.roomIdGeneration.generate(), **kwargs)
        chat_config_instance.participant.add(*participant_ids)
        chat_config_instance.save()
        return chat_config_instance
