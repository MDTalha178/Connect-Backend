from rest_framework import status
from rest_framework.decorators import action

from authentication.models import User
from authentication.serializer import SignupSerializer, LoginSerializer, VerificationSerializer
from authentication.token import AuthTokenInterface, JWTTokenAuthService
from common.utils import CustomModelView


class SignupViewSet(CustomModelView):
    """
    this class is used for signup viewlet where user can sign up
    """
    http_method_names = ('post',)
    serializer_class = SignupSerializer
    queryset = User

    def __init__(self,
                 token_service: AuthTokenInterface = JWTTokenAuthService(),
                 *args, **kwargs
                 ):
        self.token_service = token_service
        super().__init__(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        this method is used to create a signup data
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # generating a token for user
            token_response = self.token_service.generate_token(user)

            data = {**serializer.data, **token_response}
            return self.success_response(status_code=status.HTTP_201_CREATED, data=data)
        return self.failure_response(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class LoginViewSet(CustomModelView):
    http_method_names = ('post',)
    serializer_class = LoginSerializer
    queryset = User

    def __init__(
            self, token_service: AuthTokenInterface = JWTTokenAuthService(),
            *args, **kwargs
    ):
        self.token_service = token_service
        super().__init__(*args, **kwargs)

    def create(self, request, *args, **kwargs):

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():

                # generate Token
                user_obj = serializer.validated_data.get('user_obj')
                response_dict = self.token_service.generate_token(user_obj)

                return self.success_response(status_code=status.HTTP_200_OK, data=response_dict)

            return self.failure_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=serializer.errors
            )
        except Exception as e:
            return self.failure_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={'error': f'Something went wrong: {str(e)}'}
            )

    @action(methods=['post'], detail=False, url_path='verification', url_name='verification',
            serializer_class=VerificationSerializer
            )
    def verification(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_dict = self.token_service.generate_token(user)
            return self.success_response(status_code=status.HTTP_200_OK, data=response_dict)

        return self.failure_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )
