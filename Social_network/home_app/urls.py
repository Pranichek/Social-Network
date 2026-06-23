from django.urls import path
from .views import HomeView, EndRegistrationView

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('end_register/', EndRegistrationView.as_view(), name = 'end_register')
]