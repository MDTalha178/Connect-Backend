from authentication.models import User
from common.Services.DataAccessServices import DataAccessService


class UserRepository(DataAccessService):

    def __init__(self, **kwargs):
        super().__init__(User)

