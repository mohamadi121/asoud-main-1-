"""
ASGI config for asoud project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from apps.chat.routing import websocket_urlpatterns as chat_urlpatterns
from apps.notification.urls import urlpatterns as notification_urlpatterns

combined_ws_urlpatterns = chat_urlpatterns + notification_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

django_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                combined_ws_urlpatterns
            )
        )
    ),
})
