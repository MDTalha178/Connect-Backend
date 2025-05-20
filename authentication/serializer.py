import logging

from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from authentication.exception import ApplicationException
from authentication.models import User
from authentication.Repository.UserRepository import UserRepository
from chat.Services.ChatConfigurationService import ChatConfigurationService
from common.Interface.DataObjectLayer import DataObjectLayerInterface
from common.contstant import COMMUNICATION_MODE
from common.factory import VerificationFactory
from common.Generate import GenerateDigitStrategy
from common.interface import VerificationInterface, GenerateInterface


class SignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True, allow_null=False, allow_blank=False
    )

    last_name = serializers.CharField(
        required=True, allow_null=False, allow_blank=False
    )

    email = serializers.EmailField(
        required=True, allow_null=False, allow_blank=False
    )

    phone = serializers.CharField(
        required=True, allow_null=False, allow_blank=False,
        min_length=10
    )

    def __init__(self,
                 generate_otp_service: GenerateInterface = GenerateDigitStrategy(),
                 user_repo: DataObjectLayerInterface = UserRepository(),
                 *args, **kwargs):

        self.generate_otp_service: GenerateInterface = generate_otp_service
        self.user_repo = user_repo
        super().__init__(**kwargs)

    def validate_phone(self, value):
        try:
            self.user_repo.get(phone=value)
            raise serializers.ValidationError("Pone Number is already exists!")
        except ApplicationException as a:
            return value
        except Exception as e:
            return value

    def validate_email(self, value):
        try:
            self.user_repo.get(email=value)
            raise serializers.ValidationError("Email is already exists!")
        except ApplicationException as a:
            return value
        except Exception as e:
            return value

    def create(self, validated_data):
        try:
            # Generate OTP and save into database
            validated_data['email_verification_otp'] = self.generate_otp_service.generate_otp()

            if self.user_repo.create(validated_data):
                user_obj = self.user_repo.get(phone=validated_data['phone'])
                return user_obj
        except ApplicationException as application_error:
            raise serializers.ValidationError(application_error)
        except Exception as e:
            raise serializers.ValidationError("Something Went wrong")

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone',)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, allow_null=False, allow_blank=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(255)],

    )

    def __init__(self, generate_otp_service: GenerateInterface = GenerateDigitStrategy(),
                 user_repo: DataObjectLayerInterface = UserRepository(),
                 *args, **kwargs):
        self.generate_otp_service: GenerateInterface = generate_otp_service
        self.user_repo = user_repo
        super().__init__(**kwargs)

    def validate_email(self, value):
        try:
            self.user_repo.get(email=value)
            return value
        except ApplicationException as application_error:
            raise serializers.ValidationError(application_error)

    def validate(self, attrs):
        try:
            user_obj = self.user_repo.get(email=attrs.get('email'))
            if user_obj:
                attrs['user_obj'] = user_obj
                self.user_repo.update(user_obj, email_verification_otp=self.generate_otp_service.generate())
            else:
                raise serializers.ValidationError("Invalid user")
        except ApplicationException as application_error:
            raise serializers.ValidationError(application_error)
        except Exception as e:
            logging.error(e)
            raise serializers.ValidationError("Some Thing Went wrong")
        return attrs

    class Meta:
        model = User
        fields = ('email',)


class VerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, allow_null=False, allow_blank=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(255)],

    )
    otp = serializers.CharField(
        required=True, allow_null=False, allow_blank=False,
        validators=[MinLengthValidator(6), MaxLengthValidator(6)],

    )
    verification_type = serializers.ChoiceField(
        choices=COMMUNICATION_MODE, allow_null=False, default='EMAIL'
    )

    def __init__(self, *args, **kwargs):
        self.verification_strategy: VerificationInterface = VerificationFactory(
            kwargs.get('data').get('verification_type')).get_verification_strategy()
        self.user_repo = UserRepository()
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        if self.verification_strategy.verification(attrs):
            return attrs
        raise serializers.ValidationError('Invalid OTP!')

    def create(self, validated_data):
        try:
            user_obj = self.user_repo.get(email=validated_data['email'])
            if user_obj:
                return user_obj
        except Exception as e:
            raise serializers.ValidationError("Something Went Wrong!")

    class Meta:
        model = User
        fields = ('email', 'otp', 'verification_type',)


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone')
