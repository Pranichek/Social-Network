from user_app.forms import WelcomeForm
from post_app.forms import PostForm
from profile_app.models import Profile
from post_app.models import Post

from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Page
from django.template.loader import render_to_string




class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home_app/home.html'
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
            Post.objects.all().
            select_related('author').
            prefetch_related('tags', 'links', 'images').
            order_by('-id')
        )
    
class EndRegistrationView(View):
    def post(self, request, *args, **kwargs):
        form = WelcomeForm(request.POST)

        if form.is_valid():
            user = request.user
            user.username = f"@{form.cleaned_data.get('username')}"

            user_profile = Profile(
                user = request.user,
                pseudonym = form.cleaned_data.get('pseudonym')
            )

            user_profile.save()

            # user.pseudonym = form.cleaned_data.get('pseudonym')

            user.save()

            return JsonResponse({
                'success': True,
                'message': 'Дані успішно оновлено'
            })
        
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        }, status=400)

