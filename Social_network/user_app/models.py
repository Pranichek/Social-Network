# from django.db import models

# # # Create your models here.
# # class User(models.Model):
# #     name = models.CharField(max_lenght = 100)

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     username = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True
#     )

#     email = models.EmailField(unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
    