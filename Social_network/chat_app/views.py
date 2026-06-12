from .services.get_or_create_chat import get_or_create_chat
from user_app.services.friends_queries import get_friends
from .services.group_actions import create_group_service, open_chat_by_id_service 
from .services.delete_chat import delete_chat
from user_app.models import User
from .models import Chat
from .services.pagination import message_paginator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import AddChatMemberForm, CreateGroupChatForm, GroupChatUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
import secrets
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse

User = get_user_model()

class FakeProfile:
    def __init__(self, pseudonym):
        self.pseudonym = pseudonym


class FakeUser:
    def __init__(self, id, username, email, pseudonym):
        self.id = id
        self.username = username
        self.email = email
        self.userprofile = FakeProfile(pseudonym)

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
        selected_users = request.POST.getlist('users')
        if len(selected_users) < 2:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    {
                        'success': False,
                        'error': 'Для створення групи потрібно мінімум 2 користувачів'
                    }, status=400
                )
            else:
                messages.error(request, 'Для створення групи потрібно мінімум 2 користувачів')
                return redirect('chat_view')
            
        return create_group_service(request=request)
    
class DeleteChat(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        return delete_chat(request = request, chat_id = chat_id)