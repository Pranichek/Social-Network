from django.shortcuts import render , redirect
from django.views.generic import TemplateView , FormView, View
from .forms import RegistrationForm, LoginForm, ConfirmEmailForm
from django.contrib.auth.forms import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

class SettingsView(TemplateView):
    template_name = 'user_app/settings.html'


class AuthUser(TemplateView):
    template_name = 'user_app/auth.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_login'] = LoginForm
        context['form_confirm_email'] = ConfirmEmailForm
        context['form_register'] = RegistrationForm

        return context
        

class LoginView(FormView):
    template_name = 'user_app/login.html'
    form_class = LoginForm

class LogoutUser(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    

class CheckRegistration(View):
    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST)


        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Користувача успішно разеєстровано'
            })
                
        return JsonResponse({
            'success': False,
            'message': 'Помилка при реєстрації',
            'errors': form.errors.get_json_data()
        }, status = 400)
        

class CheckLogin(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return JsonResponse({
                "success": True,
                "message": "Авторизація успішна!"
            })
        
        return JsonResponse({
                "success": False,
                "message": "Авторизація неуспішна!",
                "errors": form.errors.get_json_data()
            },
            status=400
            )