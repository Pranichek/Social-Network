from django.urls import path
from .views import ChatView, SoloChatView, ChatMessagesPaginationView

urlpatterns = [
    path('', ChatView.as_view(), name = 'chat_view'),
    path('chat_with/<int:user_id>/', SoloChatView.as_view(), name = 'chat_with'),
    path('<int:chat_id>/messages/', ChatMessagesPaginationView.as_view(), name='chat_messages_pagination'),
]