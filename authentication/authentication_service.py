from typing import Optional
from rest_framework import status
from authentication.token import AuthTokenInterface, JWTTokenAuthService
from authentication.user_repository import UserRepository
from common.utils import CustomAPIResponseMixin


class AuthenticationService:

    def __init__(self, auth_strategy: AuthTokenInterface = JWTTokenAuthService()):
        self.auth_strategy = auth_strategy
        self.user_repo = UserRepository()
        self.response = CustomAPIResponseMixin()

    def authenticate(self, request) -> Optional[CustomAPIResponseMixin]:

        auth_header = request.headers.get('Authorization', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            return self.response.failure_response(
                data={'error': 'Authorization header missing or invalid'},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.split(' ')[1]

        payload = self.auth_strategy.validate_token(token)
        if not payload:
            return self.response.failure_response(
                data={'error': 'Invalid or expired token'},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        user_id = payload.get('user_id')
        if user_id is None:
            self.response.failure_response(
                data={'error': 'Invalid token payload'},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            request.user = self.user_repo.get_by_id(user_id)
        except Exception:
            return self.response.failure_response(
                data={'error': 'User not found'},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        return None