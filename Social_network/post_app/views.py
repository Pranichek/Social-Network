from .forms import PostForm
from .models import Post

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, View, ListView
from django.core.paginator import Page
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import json
# Create your views here.


class FormView(LoginRequiredMixin, FormView):
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

        html = render_to_string(
            'post_app/particles/post/post_item.html', 
            {'post': post, 'user': self.request.user}, 
            request=self.request
        )

        return JsonResponse({
            'success': True,
            'message': 'Публікація успішно створена',
            'html': html
        })
    
    # 
    def form_invalid(self, form):
        
        return JsonResponse({
            'success': False,
            'message': 'Публікація не створена'
        })
    

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_app/post.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm

        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            page_obj: Page = context["page_obj"]

            html = ""
            for post in context["posts"]:
                html += render_to_string(
                    "post_app/particles/post/post_item.html",
                    {"post": post, "user": self.request.user}, 
                    request=self.request
                )

            return JsonResponse({
                "html":html,
                "has_next": page_obj.has_next()
            })
        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self):
        return (
            Post.objects.filter(author = self.request.user).
            select_related('author').
            prefetch_related('tags', 'links', 'images').
            order_by('-id')
            )

       

class DeleteView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
            
        post_id = data.get('post_id')
        post_object : Post = get_object_or_404(Post, id=post_id)
        post_object.delete()

        return JsonResponse({
            'success': True, 
            'message': 'Публікація видалена'
        })