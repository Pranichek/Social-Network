from django.urls import path
from .views import *

urlpatterns = [
    path('settings/', SettingsView.as_view(), name = 'settings_view'),
    path('register/', RegistrationView.as_view(), name = 'registration_view'),
    path('registration/', CheckRegistration.as_view(), name='check_registration'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('check_login/', CheckLogin.as_view(), name='check_login_view'),
]