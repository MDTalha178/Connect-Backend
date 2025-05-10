from rest_framework.permissions import BasePermission

from authentication.authentication_service import AuthenticationService


class AuthenticationPermission(BasePermission):
    message = 'Authentication Failed'

    def __init__(self):
        self.auth_service = AuthenticationService()

    def has_permission(self, request, view):
        try:
            self.auth_service.authenticate(request)
            return True
        except Exception as e:
            return False