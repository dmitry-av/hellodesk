from django.urls import re_path

from . import consumers

urlpatterns = [
    re_path(r'ws/chats/(?P<pk>\d+)/$',
            consumers.ChatConsumer.as_asgi(), name='chat-websocket'),
]
