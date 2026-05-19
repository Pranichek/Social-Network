from .services.send_email import generate_mail
from .services.generate_code import generate_user_code
from user_app.services.friends_queries import *
from .models import Friendship, User


from django.views.generic import TemplateView , View
from .forms import RegistrationForm, LoginForm, ConfirmEmailForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import  login
from django.http import JsonResponse
import threading
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.template.loader import render_to_string



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
        

# class LoginView(FormView):
#     template_name = 'user_app/login.html'
#     form_class = LoginForm

class LogoutUser(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    

class CheckRegistration(View):
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        

        if form.is_valid():
            # form.save()

            code = generate_user_code()

            email_thread = threading.Thread(
                target=generate_mail, 
                kwargs={
                    'request': request, 
                    'recipient_email': request.POST.get('email'),
                    'code': code
                }
            )

            email_thread.start()

            request.session['confirm_code'] = code
            request.session['reg_data'] = {
                'email': form.cleaned_data.get('email'),
                'password': form.cleaned_data.get('password'),
                'confirm_password': form.cleaned_data.get('confirm_password')
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Користувача успішно разеєстровано'
            })
                
        return JsonResponse({
            'success': False,
            'message': 'Помилка при реєстрації',
            'errors': form.errors.get_json_data()
        }, status = 400)
    

class ConfirmEmail(View):
    def post(self, request, *args, **kwargs):
        user_code = request.POST.get('code')
        session_code = request.session.get('confirm_code')
        reg_data = request.session.get('reg_data')


        if not session_code:
            return JsonResponse({
                'success': False, 
                'message': 'Сесія закінчилася, спробуйте ще раз'
            }, status=400)

        if str(user_code) == str(session_code):

            form = RegistrationForm(reg_data)

            if form.is_valid():
                form.save() 

                del request.session['confirm_code']
                del request.session['reg_data']
            

                return JsonResponse({
                    'success': True, 
                    'message': 'Реєстрація успішна'
                })
            
            return JsonResponse({
                'success': False,
                'message': 'Помилка при підтвердженні коду',
                'errors': form.errors.get_json_data()
            }, status = 400)
        
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Неправильний код'
            }, status=400)
        

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
    

class FriendsView(LoginRequiredMixin, TemplateView):
    template_name = "user_app/friends.html"
    login_url = reverse_lazy('auth_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sections'] = {
            'requests': {
                "title": 'Запити', 
                'users': friendships_requests(self.request.user)[:3]
            },
            'recommendations': {
                "title": 'Рекомендації', 
                'users': friendships_recommendations(self.request.user)[:6]
            },
            'friends': {
                "title": 'Всі друзі',
                'users':get_friends(self.request.user)[:6]
            }
            
        }

        
        return context


    
class SectionsView(LoginRequiredMixin, View):
    def get(self, request, section, *args, **kwargs):
        if section == 'requests':
            users = friendships_requests(request.user)
        elif section == 'recommendations':
            users = friendships_recommendations(request.user)
        elif section == 'friends':
            users = get_friends(request.user)

        page_object = Paginator(users, 6).get_page(request.GET.get('page', 1))

        html = render_to_string(
            'user_app/particles/friends_page/friends_cards.html', 
            context={
                'users': page_object.object_list,
                'section': section
            }, request=request)
        
        return JsonResponse({
            'has_next_page': page_object.has_next(),
            'html': html 
        })

class ChangeStatusView(LoginRequiredMixin, View):
    def get(self, request, status, *args, **kwargs):
        id_user = request.GET.get('id', 1)
        user_object = User.objects.get(id = int(id_user))
        friendship_obj = None

        if status == 'add':
            Friendship.objects.create(
                from_user=request.user,
                to_user=user_object,
                status='pending'
            )
        

        return JsonResponse({'message': 'ok'})
       
            