from rest_framework import status
from rest_framework.exceptions import APIException


class ApplicationException(APIException):
    """Base class for all custom application exceptions."""

    def __init__(self, message="An unexpected error occurred", status_code=None):
        self.message = message
        self.default_code = message
        super().__init__(detail=self.message)


class OtpException(ApplicationException):
    """Exception raised when saving OTP fails."""

    def __init__(self,
                 message="We're having trouble reaching the OTP service. Please try again later."
                 ):
        self.message = message
        super().__init__(message=self.message, status_code=status.HTTP_400_BAD_REQUEST)


class UserException(ApplicationException):
    def __init__(self,
                 message="We're having trouble reaching the User service. Please try again later."
                 ):
        self.message = message
        super().__init__(message=self.message, status_code=status.HTTP_400_BAD_REQUEST)
