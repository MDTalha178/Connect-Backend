from django.db.models import QuerySet

from authentication.exception import OtpException, UserException
from authentication.models import User
from common.data_object_layer import DataObjectLayerInterface


class UserRepository(DataObjectLayerInterface):

    def get_data(self, **filters) -> QuerySet:
        try:
            return User.objects.filter(**filters)
        except Exception as e:
            return None

    def create(self, data) -> bool:
        try:
            User.objects.create(**data)
            return True
        except Exception as e:
            print(e)
            return False

    def update(self, data: dict) -> bool:
        try:
            id_to_update = data.pop('id')
            User.objects.filter(id=id_to_update).update(**data)
            return True
        except UserException as e:
            raise UserException()

    def delete(self, user_id: str) -> bool:
        try:
            User.objects.filter(id=user_id).delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def user_by_phone(phone: str):
        try:
            return User.objects.get(phone=phone)
        except Exception as e:
            raise UserException(
                "We couldn't find an account associated with this Phone Number. "
                "Please check for any typos or try signing up."
            )

    @staticmethod
    def get_by_email(email):
        try:
            return User.objects.get(email=email)
        except Exception as e:
            raise UserException(
                "We couldn't find an account associated with this Email. "
                "Please check for any typos or try signing up."
            )

    @staticmethod
    def get_by_id(user_id: str):
        try:
            return User.objects.get(id=user_id)
        except Exception as e:
            raise UserException("We couldn't find any account associated with this User ID")

    @staticmethod
    def save_user_otp(user_id, otp) -> bool:
        try:
            User.objects.filter(id=user_id).update(email_verification_otp=otp)
            return True
        except Exception as e:
            raise OtpException(
                "We couldn't send your OTP at the moment. "
                "Please try again shortly."
            )
