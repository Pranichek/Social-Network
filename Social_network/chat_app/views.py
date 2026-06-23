from .services.get_or_create_chat import get_or_create_chat
from user_app.services.friends_queries import get_friends
from .services.group_actions import create_group_service, open_chat_by_id_service 
from .services.delete_chat import delete_chat
from .services.pagination.pagination import message_paginator
from .services.pagination.paginator_contact import paginate_contact
from .services.pagination.pagination_messages_block import paginate_active_chats
from .services.pagination.paginations_groups import paginate_group_chats
from .services.group_actions import update_group_service
from .services.save_images import message_images

from user_app.models import User
from .models import Chat

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import AddChatMemberForm, CreateGroupChatForm, GroupChatUpdateForm
from django.urls import reverse_lazy
from django.http import HttpRequest
from django.utils import timezone


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_app/chats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_member_form'] = AddChatMemberForm()
        context['create_group_form'] = CreateGroupChatForm()
        context['group_chat_update_form'] = GroupChatUpdateForm()


        context["friends"] = get_friends(self.request.user)[:20]

        # Соло чаты
        solo_chats = Chat.objects.filter(
            users=self.request.user,
            is_group=False
        ).prefetch_related('messages', 'users')

        active_chats_data = []

        for chat in solo_chats:
            other_user = chat.users.exclude(id=self.request.user.id).first()
            if not other_user:
                continue

            message = chat.messages.order_by('-created_at').first()

            if message:
                last_message_text = message.text if message.text else 'Зображення'
                last_message_data = timezone.localtime(message.created_at).strftime('%H:%M')
            else:
                last_message_text = 'Немає повідомлень'
                last_message_data = ''

            unread_count = chat.messages.exclude(
                sender=self.request.user
            ).exclude(
                readers=self.request.user
            ).count()

            active_chats_data.append({
                'user': other_user,
                'chat': chat,
                'last_message_text': last_message_text,
                'last_message_data': last_message_data,
                'unread_count': unread_count,
            })

        # сортируем по непрочитанным, потом берём первые 10
        active_chats_data.sort(key=lambda x: x['unread_count'], reverse=True)
        context['active_chats_data'] = active_chats_data[:10]


        # Групповые чаты
        solo_group_chats = Chat.objects.filter(
            users=self.request.user,
            is_group=True
        ).prefetch_related('messages')

        group_chats_data = []

        for chat in solo_group_chats:
            message = chat.messages.order_by('-created_at').first()

            if message:
                last_message_text = message.text if message.text else 'Зображення'
                last_message_data = timezone.localtime(message.created_at).strftime('%H:%M')
            else:
                last_message_text = "Немає повідомлень"
                last_message_data = ""

            unread_count = chat.messages.exclude(
                sender=self.request.user
            ).exclude(
                readers=self.request.user
            ).count()

            group_chats_data.append({
                'chat_object': chat,
                'last_message_text': last_message_text,
                'last_message_data': last_message_data,
                'unread_count': unread_count,
            })

        group_chats_data.sort(key=lambda x: x['unread_count'], reverse=True)
        context['group_chats_data'] = group_chats_data[:10]


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

# Редагування групи
class UpdateGroupView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, chat_id, *args, **kwargs):
        return update_group_service(request = request, chat_id = chat_id)
    