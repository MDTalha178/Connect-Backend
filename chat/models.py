import uuid

from django.db import models

from authentication.models import User


# Create your models here.
class ChatConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room_name = models.CharField(blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_group_chat = models.BooleanField(default=False)
    participant = models.ManyToManyField(User, related_name='user_chat_config_set')


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_config = models.ForeignKey(ChatConfig, on_delete=models.CASCADE, related_name='chat_message_config_set')
    messages = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(User, related_name='chat_message_sender', on_delete=models.CASCADE)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
