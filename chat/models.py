import uuid
from enum import Enum
from django.db import models
from django.utils import timezone

from authentication.models import User


class ChatConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room_name = models.CharField(blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_group_chat = models.BooleanField(default=False)
    participant = models.ManyToManyField(User, related_name='user_chat_config_set')


class UserRole(Enum):
    Admin = "Admin"
    Member = "Member"

    @classmethod
    def choices(cls):
        return [(role.value, role.value) for role in cls]


class ChatParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_config = models.ForeignKey(ChatConfig, on_delete=models.CASCADE, related_name='chat_participant_config_set')
    role = models.CharField(choices=UserRole.choices(), default=UserRole.Member.value)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_participant_user_set')
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_timestamp = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_config = models.ForeignKey(ChatConfig, on_delete=models.CASCADE, related_name='chat_message_config_set')
    messages = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(User, related_name='chat_message_sender', on_delete=models.CASCADE)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
