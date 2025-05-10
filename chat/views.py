from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from authentication.models import User
from authentication.serializer import GetUserSerializer
from authentication.user_repository import UserRepository
from chat.models import ChatConfig, ChatMessage
from chat.serializer import GetChatListSerializer, GetChatSerializer
from common.permission import AuthenticationPermission
from common.utils import CustomModelView


# Create your views here.
class ChatListViewSet(CustomModelView):
    http_method_names = ('get',)
    permission_classes = (AuthenticationPermission,)
    queryset = ChatConfig
    serializer_class = GetChatListSerializer

    def __init__(self, *args, **kwargs):
        self.user_repo = UserRepository()
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.objects.filter(
            participant=self.request.user
        ).order_by('-created_at')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(self.get_queryset(), many=True,
                                               context={'user_id': self.request.user.id})
            return self.success_response(data=serializer.data)
        except Exception as e:
            return self.failure_response(data={'error': e})

    @action(methods=['get'], detail=True, url_path='first-chat',
            url_name='first_chat', serializer_class=GetChatSerializer
            )
    def get_first_chat(self, request, *args, **kwargs):
        try:
            chat_config_id = kwargs['pk']

            chat_config = get_object_or_404(
                ChatConfig.objects.prefetch_related(
                    Prefetch('participant', queryset=User.objects.exclude(id=self.request.user.id),
                             to_attr='other_participants')
                ),
                id=chat_config_id
            )
            chat_messages = ChatMessage.objects.filter(chat_config_id=chat_config_id).order_by('created_at')
            serializer = self.serializer_class(chat_messages, many=True,
                                               context={'user_id': self.request.user.id})

            return self.success_response(
                data=serializer.data, online_status=chat_config.other_participants[0].online_status
            )
        except Exception as e:
            print(e)
            return self.failure_response(data={'error': e})

    @action(methods=['get'], detail=False, url_path='user-list', url_name='user-list',
            serializer_class=GetUserSerializer)
    def get_user_list(self, request, *args, **kwargs):
        try:
            user = self.user_repo.get_data().exclude(id=self.request.user.id)
            serializer = self.serializer_class(user, many=True, context={'user_id': self.request.user.id})
            return self.success_response(data=serializer.data)
        except Exception as e:
            return self.failure_response(data={'error': e})
