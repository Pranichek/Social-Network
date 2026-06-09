from .services.get_or_create_chat import get_or_create_chat
from user_app.services.friends_queries import get_friends
from .services.group_actions import create_group_service, open_chat_by_id_service 
from user_app.models import User
from .models import Chat
from .services.pagination import message_paginator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import AddChatMemberForm, CreateGroupChatForm, GroupChatUpdateForm
from django.urls import reverse_lazy

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_app/chats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_member_form'] = AddChatMemberForm()
        context['create_group_form'] = CreateGroupChatForm()
        context['group_chat_update_form'] = GroupChatUpdateForm()
        context["friends"] = get_friends(self.request.user)

        context['active_chats'] = User.objects.filter(
            chats__users = self.request.user,
            chats__is_group = False
        ).exclude(id = self.request.user.id).distinct()

        context['group_chat'] = Chat.objects.filter(
            users = self.request.user,
            is_group = True
        ).order_by('-id')


        return context
    
class SoloChatView(View):
    login_url = reverse_lazy('auth_view')

    def post(self, request, user_id, *args, **kwargs):
        return get_or_create_chat(request = request, user_id = user_id)

# class ChatMessagesPaginationView(LoginRequiredMixin, View):
#     def get(self, request, chat_id, *args, **kwargs):
#         return message_paginator(request= request, chat_id= chat_id)
class ChatMessagesPaginationView(LoginRequiredMixin, View):
    login_url = "auth_view"

    def get(self, request, chat_id, *args, **kwargs):
        return message_paginator(request=request, chat_id=chat_id)

class OpenChatByIdView(LoginRequiredMixin, View):
    def get(self, request, chat_id, *args, **kwargs):
        return open_chat_by_id_service(request=request, chat_id=chat_id)

class CreateGroupView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return create_group_service(request=request)