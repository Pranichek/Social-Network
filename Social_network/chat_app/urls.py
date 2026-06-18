from django.urls import path
from .views import *

urlpatterns = [
    path('', ChatView.as_view(), name = 'chat_view'),
    path('chat_with/<int:user_id>/', SoloChatView.as_view(), name = 'chat_with'),
    path('<int:chat_id>/messages/', ChatMessagesPaginationView.as_view(), name='chat_messages_pagination'),
    path('open/<int:chat_id>/', OpenChatByIdView.as_view(), name='open_chat_by_id'),
    path('create_group/', CreateGroupView.as_view(), name='create_group'),
    path('delete/<int:chat_id>/', DeleteChat.as_view(), name = 'delete_chat'),

    path('contacts/', LoadContactsView.as_view(), name='load_contacts'),
    path('message_block/', LoadMessageBlockView.as_view(), name='paginate_message_block'),
    path('group_block/', LoadGroupBlockView.as_view(), name='paginate_group_block'),
    
    path('upload_images/<int:chat_id>/', MessageUploadView.as_view(), name = 'message_upload'),

    path('update_group/<int:chat_id>/', UpdateGroupView.as_view(), name='update_group'),
]