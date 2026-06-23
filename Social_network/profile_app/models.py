from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField('user_app.User', on_delete=models.CASCADE, related_name="userprofile")
    birth_date = models.DateField(null=True, blank=True)
    signature = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='profile_app/avatars/', null=True, blank=True)
    pseudonym = models.CharField(max_length=50)
    is_image_signature = models.BooleanField(default=False)
    is_text_signature = models.BooleanField(default=False)

