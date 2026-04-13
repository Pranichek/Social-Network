from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class FriendView(TemplateView):
    template_name = 'friends_app/friends.html'