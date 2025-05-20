from authentication.models import User
from chat.repository.ChatUserRepository import ChatUserRepository
from common.contstant import USER_STATUS


class ChatUserServices:
    def __init__(self):
        self.user_repo = ChatUserRepository(User)

    async def set_user_status(self, data: dict):
        user_instance = await self.user_repo.get(id=data['user_id'])
        await self.user_repo.update(user_instance, online_status=USER_STATUS[data['status']])
