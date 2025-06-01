from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied

from authentication.models import User
from authentication.serializer import GetUserSerializer
from authentication.Repository.UserRepository import UserRepository
from chat.models import ChatConfig, ChatMessage
from chat.serializer import GetChatListSerializer, GetChatSerializer, CreateChatSerializer, MuteChatSerializer, \
    GetMuteSerializer, UnMuteChatSerializer, ChatPinSerializer, VerifyChatPinSerializer, RemovePinSerializer, \
    BlockUnblockSerializerUser
from common.permission import AuthenticationPermission
from common.utils import CustomModelView


# Create your views here.
class ChatListViewSet(CustomModelView):
    http_method_names = ('get', 'post',)
    permission_classes = (AuthenticationPermission,)
    queryset = ChatConfig
    serializer_class = GetChatListSerializer

    def __init__(self, *args, **kwargs):
        self.user_repo = UserRepository()
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.objects.filter(
            participant=self.request.user
        ).order_by('-updated_at')
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

            chat_config_data = GetChatListSerializer(chat_config, many=False).data

            return self.success_response(
                data=serializer.data, online_status=chat_config.other_participants[0].online_status,
                chat_config=chat_config_data
            )
        except Exception as e:
            print(e)
            return self.failure_response(data={'error': e})

    @action(methods=['get'], detail=False, url_path='user-list', url_name='user-list',
            serializer_class=GetUserSerializer)
    def get_user_list(self, request, *args, **kwargs):
        try:
            user = self.user_repo.filter().exclude(id=self.request.user.id)
            serializer = self.serializer_class(user, many=True, context={'user_id': self.request.user.id})
            return self.success_response(data=serializer.data)
        except Exception as e:
            return self.failure_response(data={'error': e})

    @action(methods=['post'], detail=False, url_path='create-chat', url_name='create-chat',
            serializer_class=CreateChatSerializer)
    def create_chat(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
            if serializer.is_valid():
                data = serializer.save()
                data = GetChatListSerializer(data, many=False, context={'user_id': self.request.user.id})
                return self.success_response(data=data.data, message="Chat Created Successfully!")
        except Exception as e:
            return self.failure_response(data={'error': e})


class ChatActionViewSet(CustomModelView):
    http_method_names = ('post',)

    @action(methods=['post'], detail=False, url_path='mute-chat', url_name='mute_chat',
            serializer_class=MuteChatSerializer)
    def mute_chat(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
            if serializer.is_valid():
                chat_setting = serializer.save()
                chat_setting_data = GetMuteSerializer(chat_setting).data
                return self.success_response(data=chat_setting_data, message="Chat Muted Successfully!")

        except NotFound as not_found:
            return self.failure_response(data=str(not_found), message='Unable to  Mute Chat!')

        except PermissionDenied as permission:
            return self.failure_response(data=str(permission), message='Unable to  Mute Chat!')

        except Exception as e:
            return self.failure_response(data={"error": str(e)}, message="Something Went Wrong")

    @action(methods=['post'], detail=False, url_path='un-mute-chat', url_name='un_mute_chat',
            serializer_class=UnMuteChatSerializer)
    def un_mute_chat(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
            if serializer.is_valid():
                chat_setting = serializer.save()
                chat_setting_data = GetMuteSerializer(chat_setting).data
                return self.success_response(data=chat_setting_data, message="Chat Muted Successfully!")

        except NotFound as not_found:
            return self.failure_response(data=str(not_found), message='Unable to  UnMute Chat!')

        except PermissionDenied as permission:
            return self.failure_response(data=str(permission), message='Unable to  UnMute Chat!')

        except Exception as e:
            return self.failure_response(data={"error": str(e)}, message="Something Went Wrong")

    @action(methods=['post'], detail=False, url_path='set-chat-pin', url_name='set-chat-pin',
            serializer_class=ChatPinSerializer)
    def create_chat_pin(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
            if serializer.is_valid():
                chat_setting = serializer.save()
                chat_setting_data = GetMuteSerializer(chat_setting).data
                return self.success_response(data=chat_setting_data, message="M-pin Set Successfully!")
            
            return self.failure_response(data=serializer.errors, message='Unable to set M-pin Chat!')

        except NotFound as not_found:
            return self.failure_response(data=str(not_found), message='Unable to set M-pin Chat!')

        except PermissionDenied as permission:
            return self.failure_response(data=str(permission), message='Unable to set M-pin Chat!')

        except Exception as e:
            return self.failure_response(data={"error": str(e)}, message="Something Went Wrong")

    @action(methods=['post'], detail=False, url_path='verify-chat-pin', url_name='verify-chat-pin',
            serializer_class=VerifyChatPinSerializer)
    def verify_chat_pin(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
            if serializer.is_valid():
                return self.success_response(
                    data={"Chat": "Chat m-Pin verify successfully!"}, message="M-pin verify Successfully!"
                )

            return self.failure_response(data=serializer.errors, message='Unable to verify M-pin!')

        except NotFound as not_found:
            return self.failure_response(data=str(not_found), message='Unable to verify  M-pin!')

        except PermissionDenied as permission:
            return self.failure_response(data=str(permission), message='Unable to verify M-pin!')

        except Exception as e:
            return self.failure_response(data={"error": str(e)}, message="Something Went Wrong")

    @action(methods=['post'], detail=False, url_path='delete-chat-pin', url_name='delete-chat-pin',
            serializer_class=RemovePinSerializer)
    def delete_chat_pin(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
            if serializer.is_valid():
                chat_setting = serializer.save()
                chat_setting_data = GetMuteSerializer(chat_setting).data
                return self.success_response(
                    data=chat_setting_data, message="M-pin delete Successfully!"
                )

            return self.failure_response(data=serializer.errors, message='Unable to delete M-pin!')

        except NotFound as not_found:
            return self.failure_response(data=str(not_found), message='Unable to delete  M-pin!')

        except PermissionDenied as permission:
            return self.failure_response(data=str(permission), message='Unable to delete M-pin!')

        except Exception as e:
            return self.failure_response(data={"error": str(e)}, message="Something Went Wrong")

    @action(methods=['post'], detail=False, url_path='block-unblock-user', url_name='block-unblock-user',
            serializer_class=BlockUnblockSerializerUser)
    def block_and_unblock_user(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
            if serializer.is_valid():
                chat_setting = serializer.save()
                chat_setting_data = GetMuteSerializer(chat_setting).data
                return self.success_response(
                    data=chat_setting_data, message="Block or Unblock successfully"
                )

            return self.failure_response(data=serializer.errors, message='Unable to Block or Unblock!')

        except NotFound as not_found:
            return self.failure_response(data=str(not_found), message='Unable to Block or Unblock')

        except PermissionDenied as permission:
            return self.failure_response(data=str(permission), message='Unable to Block or Unblock')

        except Exception as e:
            return self.failure_response(data={"error": str(e)}, message="Something Went Wrong")
