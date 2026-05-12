from django.urls import path
from .views import FriendView

urlpatterns = [
    path('profile/', FriendView.as_view(), name = 'profile_view' )
]