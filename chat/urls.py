from django.urls import re_path
from .consumer import ChatConsumer, UserConsumer

from django.urls import path, include
from rest_framework import routers

from .views import ChatListViewSet

router = routers.DefaultRouter()

router.register('chat-list', ChatListViewSet, basename='chat_list')

urlpatterns = [
    path(r'chat/', include(router.urls)),
]

websocket_urlpatterns = [
    re_path(r'ws/chat-room/(?P<room_name>[^/]+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/user/(?P<user_id>[^/]+)/$', UserConsumer.as_asgi()),
]