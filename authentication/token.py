from abc import ABC, abstractmethod

from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from authentication.models import User


class AuthTokenInterface(ABC):

    @abstractmethod
    def generate_token(self, user: User) -> dict:
        raise NotImplementedError("Sub class should have to implement this")

    @abstractmethod
    def validate_token(self, token):
        raise NotImplementedError("Sub class should have to implement this")


class AuthTokenValidation(ABC):
    @abstractmethod
    def token_validation(self, token):
        raise NotImplementedError("Sub class should have to implement this")


class JWTAuthTokenStrategy(AuthTokenValidation):

    def token_validation(self, token):
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError, ExpiredSignatureError, InvalidTokenError):
            return None


class JWTTokenAuthService(AuthTokenInterface):

    def __init__(self, token_validation_strategy: AuthTokenValidation = JWTAuthTokenStrategy()):
        self.token_validation_strategy = token_validation_strategy

    def generate_token(self, user: User) -> dict:
        refresh_token = RefreshToken.for_user(user)
        token_dict = {
            'access_token': str(refresh_token.access_token),
            'refresh_token': str(refresh_token),
            'user_id': user.id
        }

        return token_dict

    def validate_token(self, token):
        return self.token_validation_strategy.token_validation(token)
