from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Create your views here.
class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_app/chats.html'