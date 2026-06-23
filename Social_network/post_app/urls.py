from django.urls import path
from .views import PostListView, DeleteView, FormView

urlpatterns = [
    path('forms/', FormView.as_view(), name = 'form_view'),
    path('posts/', PostListView.as_view(), name = 'post_view'),
    path('delete_post/', DeleteView.as_view(), name= "delete_post_view")
]