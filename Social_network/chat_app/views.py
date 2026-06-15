from .services.get_or_create_chat import get_or_create_chat
from user_app.services.friends_queries import get_friends
from .services.group_actions import create_group_service, open_chat_by_id_service 
from .services.delete_chat import delete_chat
from .services.pagination.pagination import message_paginator
from .services.pagination.paginator_contact import paginate_contact
from .services.pagination.pagination_messages_block import paginate_active_chats
from .services.pagination.paginations_groups import paginate_group_chats
from .services.save_images import message_images

from user_app.models import User
from .models import Chat

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import AddChatMemberForm, CreateGroupChatForm, GroupChatUpdateForm
from django.urls import reverse_lazy
from django.http import HttpRequest


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_app/chats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_member_form'] = AddChatMemberForm()
        context['create_group_form'] = CreateGroupChatForm()
        context['group_chat_update_form'] = GroupChatUpdateForm()


        context["friends"] = get_friends(self.request.user)[:20]

        context['active_chats'] = User.objects.filter(
            chats__users = self.request.user,
            chats__is_group = False
        ).exclude(id = self.request.user.id).distinct()[:10]

        context['group_chat'] = Chat.objects.filter(
            users = self.request.user,
            is_group = True
        ).order_by('-id')[:10]


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
    
class DeleteChat(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        return delete_chat(request = request, chat_id = chat_id)
    
# пагінація
class LoadContactsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return paginate_contact(request= request)
    

class LoadMessageBlockView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return paginate_active_chats(request= request)
    
class LoadGroupBlockView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return paginate_group_chats(request=request)

# Збереження зображень до повідомлень
class MessageUploadView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_view")

    def post(self, request: HttpRequest, chat_id):
        return message_images(request= request, chat_id= chat_id)