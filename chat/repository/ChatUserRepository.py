from channels.db import database_sync_to_async
from authentication.exception import UserException
from authentication.models import OnlineStatus
from common.Services.AsyncDataServices import AsyncDataAccessService


class ChatUserRepository(AsyncDataAccessService):

    @database_sync_to_async
    def user_status(self, user_id) -> bool:
        try:
            filter_query = {'id': user_id, 'online_status': OnlineStatus.ONLINE}
            if self.filter(**filter_query):
                return True
        except UserException as e:
            raise UserException()
        return False
