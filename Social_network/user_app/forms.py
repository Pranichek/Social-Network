from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='Електронна пошта', 
        max_length = 255,
        widget = forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    
    password = forms.CharField(
        label = 'Пароль',
        widget = forms.PasswordInput(attrs={
            'placeholder': 'Введи пароль', 
            'id': 'password-input'
        })
    )
    
    confirm_password = forms.CharField(
        label = 'Підтвердити пароль', 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повтори пароль',
            'id': 'password-input'
        })
    )
    
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
    email = forms.EmailField(label='Електронна пошта', max_length = 255, widget=forms.EmailInput(attrs={
        'class': 'input-with-email',
        'placeholder': 'you@example.com',
    }))
    password = forms.CharField(label = 'Пароль', widget = forms.PasswordInput(attrs={
        'class': 'input-with-eye',
        'placeholder': 'Введи пароль'
    }))
            
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username = email, password = password)
            if user is None:
                raise ValidationError('Невірний email або пароль')
        return self.cleaned_data  
    

class ConfirmEmailForm(forms.Form):
    first_number = forms.CharField(max_length = 1, widget = forms.TextInput(attrs={'placeholder': '___'}))
    second_number = forms.CharField(max_length = 1, widget = forms.TextInput(attrs={'placeholder': '___'}))
    third_number = forms.CharField(max_length = 1, widget = forms.TextInput(attrs={'placeholder': '___'}))
    fourth_number = forms.CharField(max_length = 1, widget = forms.TextInput(attrs={'placeholder': '___'}))
    fifth_number = forms.CharField(max_length = 1, widget = forms.TextInput(attrs={'placeholder': '___'}))
    sixth_number = forms.CharField(max_length = 1, widget = forms.TextInput(attrs={'placeholder': '___'}))
    

    

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
