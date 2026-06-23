from django.urls import *
from .consumers import FriendRequestConsumer

websocket_urlpatterns = [
    path('ws/friend_requests/', FriendRequestConsumer.as_asgi())
]