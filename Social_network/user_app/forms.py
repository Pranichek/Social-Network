from profile_app.models import Profile


from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label = 'Пароль',
        widget = forms.PasswordInput(attrs={
            'placeholder': 'Введи пароль', 
            'id': 'password-input'
        }),
        error_messages = {'required': 'Це поле є обов’язковим'}
    )
    
    confirm_password = forms.CharField(
        label = 'Підтвердити пароль', 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повтори пароль',
            'id': 'password-input'
        }),
        error_messages={'required': 'Будь ласка, підтвердіть пароль'}
    )

    class Meta():
        model = User
        fields = ('email',)
        labels = {
            'email': 'Електронна пошта'
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@example.com'
            })
        }

        error_messages = {
            'email': {
                'required': 'Електронна пошта обов’язкова для заповнення',
                'invalid': 'Введіть коректну адресу'
            }
        }
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email = email).exists()
        
        if user:
            raise ValidationError("Ця пошта вже зайнята")
        
        return email
            
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password and password and confirm_password:
            raise ValidationError('Паролі не співпадають')
            
        return self.cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)

        # user.username = ""
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()

        return user
            
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Електронна пошта', max_length = 255, widget=forms.EmailInput(attrs={
        'class': 'input-with-email',
        'placeholder': 'you@example.com',
    }))
    password = forms.CharField(label = 'Пароль', widget = forms.PasswordInput(attrs={
        'class': 'input-with-eye',
        'placeholder': 'Введи пароль',
        'id': 'password-input'
    }))
            
    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError("Неправильна пошта або пароль")
            
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    

class ConfirmEmailForm(forms.Form):
    first_number = forms.CharField(
        max_length = 1, 
        widget = forms.NumberInput(attrs={'placeholder': '___', 'class': 'confirm-number', 'inputmode': 'numeric'})
    )
    second_number = forms.CharField(
        max_length = 1, 
        widget = forms.NumberInput(attrs={'placeholder': '___', 'class': 'confirm-number', 'inputmode': 'numeric'})
    )
    third_number = forms.CharField(
        max_length = 1, 
        widget = forms.NumberInput(attrs={'placeholder': '___', 'class': 'confirm-number', 'inputmode': 'numeric'})
    )
    fourth_number = forms.CharField(
        max_length = 1, 
        widget = forms.NumberInput(attrs={'placeholder': '___', 'class': 'confirm-number', 'inputmode': 'numeric'})
    )
    fifth_number = forms.CharField(
        max_length = 1, 
        widget = forms.NumberInput(attrs={'placeholder': '___', 'class': 'confirm-number', 'inputmode': 'numeric'})
    )
    sixth_number = forms.CharField(
        max_length = 1, 
        widget = forms.NumberInput(attrs={'placeholder': '___', 'class': 'confirm-number', 'inputmode': 'numeric'})
    )
    

class WelcomeForm(forms.ModelForm):
    pseudonym = forms.CharField(
        max_length=50,
        label='Псевдонім автора',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть Псевдонім автора'
        }),
        error_messages={'required': 'Введіть, будь ласка, псевдонім'}
    )

    class Meta:
        model = User
        fields = ["username"]
        labels = {
            'username': 'Ім’я користувача' 
        }

        widgets = {            
            'username': forms.TextInput(attrs={
                'placeholder': '@'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        pseudonym = self.cleaned_data.get('pseudonym')

        user = User.objects.filter(username = username).exists() 

        if user:
            raise ValidationError('Користувач с таким нікнеймом вже існує')
        
        
        return username
    


    # def save(self, commit = True):
    #     user = self.request.user

    #     user.username = ""
    #     user.set_password(self.cleaned_data.get('password'))
        
    #     if commit:
    #         user.save()

    #     return user
        
        