from django.urls import re_path
from apps.chat.consumers.user_consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^api/v1/user/chat/room/(?P<room_name>[^/]+)/connect/$', 
    ChatConsumer.as_asgi()),
]
