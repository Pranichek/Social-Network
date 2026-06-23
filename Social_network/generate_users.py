import os
import django

# 1. Инициализация Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Social_network.settings')
django.setup()

# -------------------------------------------------------------------

import random
import string
from datetime import date, timedelta
from django.contrib.auth import get_user_model

# Импортируем модели Profile и Friendship. 
# ВНИМАНИЕ: убедитесь, что 'user_app' — это правильное название приложения для модели Friendship.
from profile_app.models import Profile  
from user_app.models import Friendship 

User = get_user_model()

# Списки для генерации имен
FIRST_NAMES = ['Alex', 'Katya', 'Ivan', 'Elena', 'Dmitry', 'Olga', 'Sergey', 'Anna', 'Vlad', 'Maria']
LAST_NAMES = ['Smith', 'Ivanov', 'Petrov', 'Smirnov', 'Black', 'White', 'Johnson', 'Williams']
ADJECTIVES = ['Super', 'Mega', 'Cool', 'Dark', 'Light', 'Fast', 'Smart']

def generate_random_string(length=6):
    """Генерирует случайную строку из букв и цифр для уникальности"""
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def generate_random_date(start_year=1980, end_year=2010):
    """Генерирует случайную дату рождения"""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)

def populate_database(count=40):
    print(f"Начинаем генерацию {count} пользователей...")
    
    target_email = 'vovagrinchenko19@gmail.com'
    
    # 1. Находим аккаунт, с которым все будут дружить
    try:
        main_user = User.objects.get(email=target_email)
    except User.DoesNotExist:
        print(f"\n❌ ОШИБКА: Пользователь с email {target_email} не найден!")
        print("Сначала зарегистрируйте этот аккаунт на сайте, а затем запускайте скрипт.\n")
        return
    
    created_count = 0
    while created_count < count:
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        
        # Генерируем уникальные данные
        unique_suffix = generate_random_string(5)
        username = f"{fname}_{lname}_{unique_suffix}".lower()
        email = f"{username}@example.com"
        
        if User.objects.filter(email=email).exists():
            continue
            
        # 2. Создаем пользователя
        user = User.objects.create(
            username=username,
            email=email,
            first_name=fname,
            last_name=lname
        )
        user.set_password('testpassword123') 
        user.save()

        # 3. Создаем профиль
        pseudonym = f"{random.choice(ADJECTIVES)}{fname}"
        signature = f"Привет! Я {fname}, это моя случайная подпись: {generate_random_string(8)}."
        
        Profile.objects.create(
            user=user,
            birth_date=generate_random_date(),
            signature=signature,
            pseudonym=pseudonym,
            is_image_signature=random.choice([True, False]),
            is_text_signature=random.choice([True, False])
        )
        
        # 4. Создаем связь в таблице Friendship
        # Ставим status='accepted', чтобы дружба была сразу подтверждена
        Friendship.objects.create(
            from_user=user,
            to_user=main_user,
            status='accepted'
        )
        
        created_count += 1
        print(f"[{created_count}/{count}] Создан: {email} | Сразу добавлен в друзья к {target_email}")

    print("\n✅ Генерация успешно завершена!")

# Запускаем функцию
populate_database(10)