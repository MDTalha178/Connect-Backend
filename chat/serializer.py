from rest_framework import serializers

from authentication.serializer import GetUserSerializer
from chat.Services.ChatConfigurationService import ChatConfigurationService
from chat.models import ChatMessage, ChatConfig


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


class GetChatListSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

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

    class Meta:
        model = ChatConfig
        fields = ('id', 'profile', 'last_message', 'chat_room_name', 'sender', 'sender', 'unread_count')


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
