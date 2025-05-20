from chat.repository.ChatRepository import ChatRepository


class ChatServices:
    def __init__(self):
        self.chat_repo = ChatRepository()

    async def save_chat(self, **data):
        await self.chat_repo.create(**data)

    async def update_read_un_read_count(self, group_name, sender_id, receiver_id):
        await self.chat_repo.update_read_status(receiver_id, sender_id, group_name)
