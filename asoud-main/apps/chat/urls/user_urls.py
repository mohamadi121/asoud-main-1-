from django.urls import path

from apps.chat.consumers.user_consumers import ChatConsumer

app_name = 'chat_user'

urlpatterns = [
    path(
        'room/<str:room_name>/connect/',
        ChatConsumer.as_asgi(),
        name='room-connect',
    ),
]
