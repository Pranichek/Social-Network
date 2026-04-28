from django.core.mail import send_mail 
from django.conf import settings
from django.http import HttpRequest


def generate_mail(request: HttpRequest, recipient_email: str, code: str):
    subject = 'Код підтвердження пошти'
    message = f'Код підтвердження: {code}\nВведіть цей код у поля'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    
    

    try:
        send_mail(
            subject = subject,
            message = message,
            from_email = email_from,
            recipient_list = recipient_list,
            fail_silently = False
        )
    except Exception as error:
        print(f'Помилка при надсланні: {error}')

