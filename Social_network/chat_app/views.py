from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import AddChatMemberForm, CreateGroupChatForm, GroupChatUpdateForm
from user_app.services.friends_queries import get_friends


# Create your views here.
class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_app/chats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_member_form'] = AddChatMemberForm()
        context['create_group_form'] = CreateGroupChatForm()
        context['group_chat_update_form'] = GroupChatUpdateForm()
        context["friends"] = get_friends(self.request.user)


        return context
