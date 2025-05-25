from rest_framework import serializers
from chat.Services.ChatSettingService import ChatSettingService


class ChatPinSerializerValidation:

    def __init__(self, validation=None, context=None):
        self.validation = validation or dict()
        self.chat_setting_service = ChatSettingService()
        self.context = context or {}

    def set_context(self, serializer):
        self.context = serializer.context

    def __call__(self, data):

        # Pin Validation
        if 'chat_pin_validation' in self.validation:
            self.validate_chat_pin(
                data.get('chat_pin'),
                data.get('confirm_chat_pin')
            )

            self.pin_already_set(data)

    @staticmethod
    def validate_chat_pin(pin, confirm_pin):
        errors = {}
        if pin != confirm_pin:
            errors['chat_pin'] = 'Chat pins do not match.'

        if len(str(pin)) < 6 or len(str(pin)) > 6:
            errors['chat_pin'] = 'Chat pin must be 6 digits.'

        if errors:
            raise serializers.ValidationError(errors)

    def pin_already_set(self, data):
        errors = {}
        instance = self.chat_setting_service.chat_setting_repo.get(
            action_by_id=self.context.get('user_id'),
            action_for_id=data.get('target_user_id'),
            chat_config_id=data.get('chat_config'),
            is_chat_pin_set=True

        )
        if instance:
            errors['chat_pin'] = 'M-pin Already has been set for this chat'
            raise serializers.ValidationError(errors)
