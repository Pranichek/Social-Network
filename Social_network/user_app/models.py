from django.db import models

# # Create your models here.
# class User(models.Model):
#     name = models.CharField(max_lenght = 100)

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name = 'sent_friendships', on_delete = models.CASCADE)
    to_user = models.ForeignKey(User, related_name = 'received_friendships', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length= 20, default='pending')


    class Meta:
        unique_together = ('from_user', 'to_user')