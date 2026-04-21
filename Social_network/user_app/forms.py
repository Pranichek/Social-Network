from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


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
            
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username = email, password = password)
            if user is None:
                raise ValidationError('Невірний email або пароль')
        return self.cleaned_data 
    

class ConfirmEmailForm(forms.Form):
    first_number = forms.CharField(max_length=1)
    second_number = forms.CharField(max_length=1)
    third_number = forms.CharField(max_length=1)
    fourth_number = forms.CharField(max_length=1)
    fifth_number = forms.CharField(max_length=1)
    sixth_number = forms.CharField(max_length=1)
    

    

class UserForm(forms.Form):
    author = forms.CharField(
        label= "Псевдонім автора",
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть Псевдонім автора',
            'class': 'form-input'
        })
    )
    username = forms.CharField(
        label= "Ім'я користувача",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'username'
        })
    )        
