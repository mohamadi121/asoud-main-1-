from django.urls import path
from apps.notification.consumers import NotificationConsumer

urlpatterns = [
    path(
        "ws/notifications", 
        NotificationConsumer.as_asgi()
    ),
]