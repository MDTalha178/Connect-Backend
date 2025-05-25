from chat.repository.ChatSettingRepostory import ChatSettingRepository


class ChatSettingService:
    def __init__(self):
        self.chat_setting_repo = ChatSettingRepository()

    def mute_chat(self, user_id, target_user_id, chat_config):
        return self.chat_setting_repo.mute_chat(user_id, target_user_id, chat_config)

    def un_mute_chat(self, user_id, target_user_id, chat_config):
        return self.chat_setting_repo.un_mute_chat(user_id, target_user_id, chat_config)

    def set_chat_pin(self, user_id, target_user_id, chat_config, pin):
        return self.chat_setting_repo.set_chat_pin(
            user_id,
            target_user_id,
            chat_config,
            pin
        )
