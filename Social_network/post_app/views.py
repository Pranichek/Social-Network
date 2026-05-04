from .forms import PostForm

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.http import JsonResponse
# Create your views here.

class PostView(LoginRequiredMixin, FormView):
    template_name = 'post_app/post.html'
    form_class = PostForm
    login_url = reverse_lazy('auth_view')

    # 
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == 'POST':
            kwargs['links'] = self.request.POST.getlist('links')
            kwargs['images'] = self.request.FILES.getlist('images')
            
        return kwargs
    # 
    def form_valid(self, form):
        post = form.save(author=self.request.user)

        return JsonResponse({
            'success': True,
            'message': 'Публікація успішно створена'
        })
    
    # 
    def form_invalid(self, form):
        
        return JsonResponse({
            'success': False,
            'message': 'Публікація не створена'
        })
       



