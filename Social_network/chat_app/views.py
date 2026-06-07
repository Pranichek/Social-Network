from .services.get_or_create_chat import get_or_create_chat
from .services.pagination import message_paginator
from user_app.services.friends_queries import get_friends
from .models import Chat
from user_app.models import User


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import AddChatMemberForm, CreateGroupChatForm, GroupChatUpdateForm
<<<<<<< HEAD
from django.urls import reverse_lazy
=======
from user_app.services.friends_queries import get_friends
>>>>>>> 327763feee5ff2d1497068b77b46fb689f75891b


# Create your views here.
class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_app/chats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_member_form'] = AddChatMemberForm()
        context['create_group_form'] = CreateGroupChatForm()
        context['group_chat_update_form'] = GroupChatUpdateForm()
<<<<<<< HEAD
        context["friends"] = get_friends(self.request.user)

        context['active_chats'] = User.objects.filter(
            chats__users = self.request.user,
            chats__is_group = False
        ).exclude(id = self.request.user.id).distinct()


=======
        context['users_list'] = get_friends(self.request.user)
>>>>>>> 327763feee5ff2d1497068b77b46fb689f75891b
        return context
    
class SoloChatView(View):
    login_url = reverse_lazy('auth_view')

    def post(self, request, user_id, *args, **kwargs):
        return get_or_create_chat(request = request, user_id = user_id)

class ChatMessagesPaginationView(LoginRequiredMixin, View):
    def get(self, request, chat_id, *args, **kwargs):
        return message_paginator(request= request, chat_id= chat_id)
    
    