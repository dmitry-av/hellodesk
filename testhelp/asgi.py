import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .channelsmiddleware import JwtAuthMiddlewareStack

import chats.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testhelp.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JwtAuthMiddlewareStack(
        URLRouter(
            chats.routing.urlpatterns
        )
    ),
})
