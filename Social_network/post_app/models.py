from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__ (self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='tags')

    def __str__ (self):
        return self.name

class Link(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()

    def __str__ (self):
        return self.url
