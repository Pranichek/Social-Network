from django.urls import path
from .consumers import ChatConsumer, OnlineStatusConsumer

websocket_urlpatterns = [
    path(route='chat/<int:chat_id>/', view=ChatConsumer.as_asgi()),
    path('chat/online/', OnlineStatusConsumer.as_asgi())
]