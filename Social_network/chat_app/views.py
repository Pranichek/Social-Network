from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Create your views here.
class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_app/chats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['private_messages'] = 'private_messages'
        context['group_messages'] = 'group_messages'
        
        return context