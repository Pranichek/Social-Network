from django.urls import path
from .views import PostView, DeleteView

urlpatterns = [
    path('posts/', PostView.as_view(), name = 'post_view'),
    path('delete_post/', DeleteView.as_view(), name= "delete_post_view")
]