from chat.repository.ChatSettingRepostory import ChatSettingRepository


class ChatSettingService:
    def __init__(self):
        self.__chat_setting_repo = ChatSettingRepository()

    def mute_chat(self, user_id, target_user_id, chat_config):
        return self.__chat_setting_repo.mute_chat(
            user_id,
            target_user_id,
            chat_config
        )

    def un_mute_chat(self, user_id, target_user_id, chat_config):
        return self.__chat_setting_repo.un_mute_chat(
            user_id,
            target_user_id,
            chat_config
        )

    def set_chat_pin(self, user_id, target_user_id, chat_config, pin):
        return self.__chat_setting_repo.set_chat_pin(
            user_id,
            target_user_id,
            chat_config,
            pin
        )

    def block_and_unlock_user(self,  user_id, target_user_id, chat_config, action_type, reason):
        return self.__chat_setting_repo.block_and_unblock_chat(
            user_id,
            target_user_id,
            chat_config,
            action_type,
            reason
        )

    def delete_chat_pin(self, user_id, target_user_id, chat_config) -> bool:
        return self.__chat_setting_repo.delete_chat(
            user_id,
            target_user_id,
            chat_config
        )

    def get_chat_setting_repo(self):
        return self.__chat_setting_repo
