"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
import apps.auction.routing as auct
from apps.auction.WebSocketTokenMiddleware import TokenAuthMiddlewareStack
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.development")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator( 
        TokenAuthMiddlewareStack(
            URLRouter([
                path('ws/api/v1', URLRouter([
                    *auct.auction_websocket_urlpatterns,
                ])),
            ])
        )
    )
})
