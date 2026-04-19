from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label="Електронна пошта",
        max_length=255,
        widget=forms.EmailInput(attrs={"placeholder": "Введіть email"}),
    )
    password = forms.CharField(
        label="Введи пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Введіть пароль", 'class': 'password-field'}),
    )
    confirm_password = forms.CharField(
        label="Повтори пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Повторіть пароль", 'class': 'password-field'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(username=email).exists()

        if user:
            raise ValidationError("Ця пошта вже зайнята")

        return email

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password and password and confirm_password:
            raise ValidationError("Паролі не співпадають")

        return self.cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label="you@example.com", max_length=255)
    password = forms.CharField(label="Введи пароль", widget=forms.PasswordInput)
