from .services.get_or_create_chat import get_or_create_chat
from user_app.services.friends_queries import get_friends
from .services.group_actions import create_group_service, open_chat_by_id_service 
from .services.delete_chat import delete_chat
from user_app.models import User
from .models import Chat
from .services.pagination import message_paginator
from .models import Message, MessageImage

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import AddChatMemberForm, CreateGroupChatForm, GroupChatUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpRequest

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


        context["friends"] = get_friends(self.request.user)[:20]

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
    
class DeleteChat(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        return delete_chat(request = request, chat_id = chat_id)
    
# пагінація
class LoadContactsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        friends_list = get_friends(request.user)
        
        paginator = Paginator(friends_list, 20)
        
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return JsonResponse({
                'html': '',
                'has_next': False
            })

        html = render_to_string(
            'chat_app/particles/contacts_list.html', 
            {'friends': page_obj.object_list}, 
            request=request
        )

        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next()
        })
    
class MessageUploadView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth_view")

    def post(self, request: HttpRequest, chat_id):
        if not Chat.objects.filter(id= chat_id, users= request.user).exists():
            return JsonResponse({
                'success': False
            }, status= 403) 
        
        text = request.POST.get('text', "").strip()
        images = request.FILES.getlist('images')

        if not text and not images:
            return JsonResponse({
                'success': False
            }, status= 400)
        
        message = Message.objects.create(
            chat_id= chat_id,
            sender= request.user,
            text= text
        )

        for image in images:
            MessageImage.objects.create(message= message, image= image)

        image_urls = [image.image.url for image in message.images.all()]

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{chat_id}',
            {
                'type': 'send_chat_message',
                'id': message.id,
                'message_text': message.text,
                'sender': message.sender.username,
                'created_at': timezone.localtime(message.created_at).isoformat(),
                'images': image_urls,
                'is_current_user': True,
            }
        )
        return JsonResponse({
            'success': True
        })
