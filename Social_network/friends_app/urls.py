from django.urls import path
from .views import FriendView

urlpatterns = [
    path('friends/', FriendView.as_view(), name = 'friends_view' )
]