from authentication.Repository.UserRepository import UserRepository
from common.interface import VerificationInterface


class EmailOtpVerificationStrategy(VerificationInterface):

    def __init__(self):
        self.user_repo = UserRepository()

    def verification(self, data) -> bool:
        verification_dict = {
            'email_verification_otp': data['otp'],
            'email': data['email']
        }

        user_obj = self.user_repo.get(**verification_dict)
        if user_obj:
            self.update_verification_process(user_obj)
            return True

        return False

    def update_verification_process(self, user_obj):
        self.user_repo.update(user_obj, email_verification_otp=None, email_verified=True)


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
