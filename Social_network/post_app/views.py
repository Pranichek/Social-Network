from .forms import PostForm
from .models import Post

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
# Create your views here.


class PostView(LoginRequiredMixin, FormView):
    template_name = 'post_app/post.html'
    form_class = PostForm
    login_url = reverse_lazy('auth_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.request.user.user_posts.all().order_by('-id')

        return context

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
       

class DeleteView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
            
        post_id = data.get('post_id')
        post_object : Post = get_object_or_404(Post, id=post_id)
        post_object.delete()
        return JsonResponse({'message': request.POST})