from chat.repository.ChatConfigurationRepository import ChatConfigurationRepository


class ChatConfigurationService:

    def __init__(self):
        self.chat_config_repo = ChatConfigurationRepository()

    def create_chat(self, **kwargs):
        return self.chat_config_repo.create_chat(**kwargs)
