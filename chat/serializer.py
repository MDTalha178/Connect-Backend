from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, NotFound
from authentication.serializer import GetUserSerializer
from chat.Services.ChatConfigurationService import ChatConfigurationService
from chat.Services.ChatSettingService import ChatSettingService
from chat.models import ChatMessage, ChatConfig, ChatSetting
from chat.Validation.SerializerValidation.ChatPinSerializerValidation import ChatPinSerializerValidation


class GetChatSerializer(serializers.ModelSerializer):
    is_sender = serializers.SerializerMethodField()

    def get_is_sender(self, obj):
        is_sender = False
        if self.context.get('user_id') == obj.sender.id:
            is_sender = True
        return is_sender

    class Meta:
        model = ChatMessage
        fields = ('id', 'messages', 'sender', 'is_sender', 'created_at',)


class GetMuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSetting
        fields = ('id', 'chat_config', 'action_by', 'action_for', 'chat_mute', 'chat_block', 'is_chat_pin_set',)


class GetChatListSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    is_chat_mute = serializers.SerializerMethodField()

    def get_sender(self, obj):
        return str(self.context.get('user_id', ''))

    def get_profile(self, obj):
        login_user = self.context.get('user_id')
        participant = obj.participant.all().exclude(id=login_user)
        return GetUserSerializer(participant[0], many=False).data

    @staticmethod
    def get_last_message(obj):
        last_message = obj.chat_message_config_set.order_by('-created_at').first()
        if last_message:
            return {
                'id': last_message.id,
                'message': last_message.messages,
                'sender_id': last_message.sender.id,
                'created_at': last_message.created_at,
                'read_at': last_message.read_at
            }
        return last_message

    def get_unread_count(self, obj):
        user_id = self.context.get('user_id')
        # Count messages where read_at is None and sender is not the current user
        return obj.chat_message_config_set.filter(
            read_at__isnull=True
        ).exclude(
            sender__id=user_id
        ).count()

    def get_is_chat_mute(self, obj):
        chat_setting_service = ChatSettingService()
        login_user = self.context.get('user_id')
        participant = obj.participant.all().exclude(id=login_user)
        chat_setting = chat_setting_service.chat_setting_repo.get(
            chat_config_id=obj.id,
            action_by_id=login_user,
            action_for_id=participant[0].id
        )
        if chat_setting:
            return GetMuteSerializer(chat_setting, many=False).data
        return None

    class Meta:
        model = ChatConfig
        fields = ('id', 'profile', 'last_message', 'chat_room_name', 'sender', 'sender',
                  'unread_count', 'is_chat_mute',
                  )


class CreateChatSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListSerializer(
        child=serializers.CharField(),
        required=True, allow_null=False, allow_empty=False
    )
    is_group_chat = serializers.BooleanField(
        default=False
    )

    def __init__(self, chat_config_service=ChatConfigurationService(), **kwargs):
        self.chat_config_service = chat_config_service
        super().__init__(**kwargs)

    def create(self, validated_data):
        try:
            participant_ids: list = validated_data['participant_ids']
            participant_ids.append(str(self.context.get('user_id')))
            validated_data['participant_ids'] = participant_ids
            chat_config_instance = self.chat_config_service.create_chat(**validated_data)
            return chat_config_instance
        except Exception as e:
            raise serializers.ValidationError("Something went wrong")

    class Meta:
        model = ChatConfig
        fields = ('participant_ids', 'is_group_chat',)


class MuteChatSerializer(serializers.ModelSerializer):
    target_user_id = serializers.CharField(
        required=True, allow_blank=False, allow_null=False
    )
    chat_config = serializers.CharField(
        required=True, allow_blank=False, allow_null=False
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_setting_service = ChatSettingService()
        self.chat_config_service = ChatConfigurationService()

    def validate(self, attrs):
        chat_config = self.chat_config_service.chat_config_repo.get(
            id=attrs.get('chat_config'),
        )

        if not chat_config:
            raise NotFound(
                detail="Chat Configuration ID Not Found!"
            )

        participant_list = self.chat_config_service.get_participant_list(chat_config)

        if str(self.context.get('user_id')) not in participant_list:
            raise PermissionDenied(
                detail="User is not Authorized to Mute this chat!",
            )

        if attrs.get('target_user_id') not in participant_list:
            raise NotFound(
                detail='Target ID Not Found',
            )

        return attrs

    def create(self, validated_data):
        try:
            chat_setting = self.chat_setting_service.mute_chat(
                str(self.context.get('user_id')), validated_data.get('target_user_id'),
                validated_data.get('chat_config')
            )
            return chat_setting
        except Exception as e:
            raise serializers.ValidationError(e)

    class Meta:
        model = ChatSetting
        fields = ('target_user_id', 'chat_config',)


class UnMuteChatSerializer(MuteChatSerializer):

    def create(self, validated_data):
        try:
            chat_setting = self.chat_setting_service.un_mute_chat(
                str(self.context.get('user_id')),
                validated_data.get('target_user_id'),
                validated_data.get('chat_config')
            )
            return chat_setting

        except NotFound as not_found:
            raise NotFound(
                "Chat Configuration is Invalid!"
            )
        except Exception as e:
            raise serializers.ValidationError(e)

    class Meta:
        model = ChatSetting
        fields = ('target_user_id', 'chat_config',)


class ChatPinSerializer(MuteChatSerializer):
    chat_pin = serializers.IntegerField(
        required=True, allow_null=False
    )
    confirm_chat_pin = serializers.IntegerField(
        required=True, allow_null=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for validator in self.Meta.validators:
            if isinstance(validator, ChatPinSerializerValidation):
                validator.context = self.context

    def create(self, validated_data):
        try:
            chat_setting = self.chat_setting_service.set_chat_pin(
                str(self.context.get('user_id')),
                validated_data.get('target_user_id'),
                validated_data.get('chat_config'),
                validated_data.get('chat_pin')
            )
            return chat_setting
        except Exception as e:
            raise serializers.ValidationError("Something went Wrong")

    class Meta:
        model = ChatSetting
        fields = ('target_user_id', 'chat_config', 'chat_pin', 'confirm_chat_pin')
        validators = [
            ChatPinSerializerValidation(
                validation={'chat_pin_validation'},
            )
        ]
        extra_kwargs = {
            'confirm_chat_pin': {'write_only': True}
        }
