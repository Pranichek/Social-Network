from django.urls import path
from .consumers import ChatConsumer, OnlineStatusConsumer, UnreadConsumer

websocket_urlpatterns = [
    path(route='chat/<int:chat_id>/', view=ChatConsumer.as_asgi()),
    path('chat/online/', OnlineStatusConsumer.as_asgi()),
    path('chat/unread/', UnreadConsumer.as_asgi())
    # path('chat/notifications/', NotificationConsumer.as_asgi()),
]