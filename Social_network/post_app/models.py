from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__ (self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, null=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='tags')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class PostLink(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()

    def __str__ (self):
        return self.url

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    original_image = models.ImageField(upload_to='post_app/original_images/', null=True, blank=True)
    compressed_image = models.ImageField(upload_to='post_app/compressed_images/', null=True, blank=True)

    def __str__(self):
        return self.original_image.name