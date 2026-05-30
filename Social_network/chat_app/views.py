from user_app.services.friends_queries import get_friends
from user_app.models import User
from .models import Chat


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import AddChatMemberForm, CreateGroupChatForm, GroupChatUpdateForm
from django.urls import reverse_lazy
from django.http import JsonResponse

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
    
class SoloChatView(View):
    login_url = reverse_lazy('auth_view')

    def post(self, request, user_id, *args, **kwargs):
        current_user = request.user
        other_user = User.objects.get(id = user_id)
        friends = get_friends(current_user=current_user)

        if other_user not in friends:
            return JsonResponse({
                'success': False,
            }, status = 403)
        
        user_chat_ids = Chat.objects.filter(users = current_user, is_group = False).values_list("id", flat = True)
        chat = Chat.objects.filter(id__in = user_chat_ids, users = other_user, is_group = False).first()

        if chat is None:
            chat = Chat.objects.create(is_group = False)
            chat.users.add(current_user, other_user)

        return JsonResponse({"success": True, "chat_id": chat.id})