from user_app.forms import WelcomeForm


from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home_app/home.html'

    

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

