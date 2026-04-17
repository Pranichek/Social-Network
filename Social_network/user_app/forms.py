from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    email = forms.EmailField(label='you@example.com', max_length = 255)
    password = forms.CharField(label = 'Введи пароль', widget = forms.PasswordInput)
    confirm_password = forms.CharField(label = 'Повтори пароль', widget = forms.PasswordInput)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(username = email).exists()
        
        if user:
            raise ValidationError("Ця пошта вже зайнята")
        
        return email
            
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password and password and confirm_password:
            raise ValidationError('Паролі не співпадають')
            
        return self.cleaned_data
            
class LoginForm(forms.Form):
    email = forms.EmailField(label='you@example.com', max_length = 255)
    password = forms.CharField(label = 'Введи пароль', widget = forms.PasswordInput)
            
        

