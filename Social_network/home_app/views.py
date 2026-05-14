from user_app.forms import WelcomeForm
from post_app.forms import PostForm

from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string

class HomeView(LoginRequiredMixin, FormView):
    template_name = 'home_app/home.html'
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

    

class EndRegistrationView(View):
    def post(self, request, *args, **kwargs):
        form = WelcomeForm(request.POST)

        if form.is_valid():
            user = request.user
            user.username = f"@{form.cleaned_data.get('username')}"
            user.pseudonym = form.cleaned_data.get('pseudonym')
            user.save()

            return JsonResponse({
                'success': True,
                'message': 'Дані успішно оновлено'
            })
        
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        }, status=400)

