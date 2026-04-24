from django.shortcuts import render , redirect
from django.views.generic import TemplateView , FormView, View
from .forms import RegistrationForm, LoginForm, ConfirmEmailForm
from django.contrib.auth.forms import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

class SettingsView(TemplateView):
    template_name = 'user_app/settings.html'

# class RegistrationView(FormView):
#     template_name = 'user_app/registration.html'
#     form_class = RegistrationForm

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
            'message': form.errors.get_json_data()
        }, status = 400)
        

            
        #     data = request.POST
        #     email = data.get('email')
        #     password = data.get('password')

        #     User.objects.create_user(username = email, password = password)
        #     return redirect('login_view')
            
        # return render(request, 'user_app/registration.html', {'form': form})

class CheckLogin(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            data = request.POST
            email = data.get('email')
            password = data.get('password')

            user = authenticate(request, username = email, password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'user_app/auth.html', {'form': form})