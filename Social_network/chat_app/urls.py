from django.urls import path
from .views import ChatView, SoloChatView

urlpatterns = [
    path('', ChatView.as_view(), name = 'chat_view'),
    path('chat_with/<int:user_id>/', SoloChatView.as_view(), name = 'chat_with'),
]