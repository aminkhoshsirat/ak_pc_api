from django.urls import re_path
from apps.notification.consumers import NotificationConsumer
from apps.chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/notification/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]
