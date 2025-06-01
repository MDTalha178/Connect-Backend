from rest_framework.exceptions import NotFound

from chat.models import ChatSetting
from common.Services.DataAccessServices import DataAccessService


class ChatSettingRepository(DataAccessService):

    def __init__(self):
        super().__init__(ChatSetting)

    def mute_chat(self, user_id, target_user_id, chat_config) -> ChatSetting:
        instance = self.idempotent_update(
            {'action_by_id': user_id, 'chat_config_id': chat_config},
            action_for_id=target_user_id,
            chat_mute=True

        )
        return instance

    def un_mute_chat(self, user_id, target_user_id, chat_config):
        instance = self.get(
            action_by_id=user_id,
            action_for_id=target_user_id,
            chat_config_id=chat_config
        )
        if instance:
            self.update(instance=instance, chat_mute=False)
            return instance
        raise NotFound(
            detail='Chat Configuration ID Not Found!',
        )

    def set_chat_pin(self, user_id, target_user_id, chat_config, pin):
        instance = self.idempotent_update(
            {'action_by_id': user_id, 'chat_config_id': chat_config},
            action_for_id=target_user_id,
            chat_pin=pin,
            is_chat_pin_set=True
        )
        return instance

    def delete_chat(self, user_id, target_user_id, chat_config):
        instance = self.idempotent_update(
            {'action_by_id': user_id, 'chat_config_id': chat_config},
            action_for_id=target_user_id,
            chat_pin=None,
            is_chat_pin_set=False
        )
        if instance:
            return instance

        raise NotFound(
            detail='Chat Pin not found in our system',
        )

    def block_and_unblock_chat(self, user_id, target_user_id, chat_config, action_type, reason):
        instance = self.idempotent_update(
            {'action_by_id': user_id, 'chat_config_id': chat_config},
            action_for_id=target_user_id,
            chat_block=action_type
        )
        if instance:
            return instance

        raise NotFound(
            detail='Chat Configuration ID Not Found!',
        )
