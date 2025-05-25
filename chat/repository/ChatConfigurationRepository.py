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

    @staticmethod
    def get_participant_list(chat_config: ChatConfig):
        participant_list = list(chat_config.participant.values_list('id', flat=True))
        return list(map(lambda part_id: str(part_id), participant_list))
