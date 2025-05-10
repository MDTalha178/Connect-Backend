from authentication.user_repository import UserRepository
from common.interface import VerificationInterface


class EmailOtpVerificationStrategy(VerificationInterface):

    def __init__(self):
        self.user_repo = UserRepository()

    def verification(self, data) -> bool:
        verification_dict = {
            'email_verification_otp': data['otp'],
            'email': data['email']
        }
        if self.user_repo.get_data(**verification_dict):
            return True
        return False


class SMSOtpVerificationStrategy(VerificationInterface):

    def __init__(self):
        self.user_repo = UserRepository()

    def verification(self, data) -> bool:
        verification_dict = {
            'email_verification_otp': data['otp'],
            'email': data['email']
        }
        if self.user_repo.get_data(**verification_dict):
            return True
        return False
