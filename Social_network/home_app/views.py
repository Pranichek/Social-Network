from user_app.forms import WelcomeForm
from user_app.models import User


from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home_app/home.html'

    
class EndRegistrationView(View):
    def post(self, request, *args, **kwargs):
        form = WelcomeForm(request.POST)

        if form.is_valid():
            user = User.objects.get(email = request.user.email)

            user.username = request.POST.get('username')
            user.pseudonym = request.POST.get('pseudonym')

            # Сохраняем изменения
            user.save()
            # 1. commit=False создает объект, но не сохраняет в БД
            # user_instance = form.save(commit=False)
            
            # # 2. Перезаписываем данные вручную
            # user_instance.user = request.user # Связываем с юзером
            # user_instance.username = request.POST.get('username') # Пример изменения поля
            # user_instance.pseudonym = request.POST.get('pseudonym')
            
            # # 3. Сохраняем в БД
            # user_instance.save() 

            print('Користувач задав юзернейм')
            
        return redirect('home')

