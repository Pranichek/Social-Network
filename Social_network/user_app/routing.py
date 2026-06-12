from django.urls import path
from .consumers import UserStatusConsumer

websocket_urlpatterns = [
    path(route='ws/status/', view=UserStatusConsumer.as_asgi()) 
]