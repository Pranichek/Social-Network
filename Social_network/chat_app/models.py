from django.db import models

# Create your models here.

class Chat(models.Model):
    name = models.CharField(max_length = 30, blank = True, null = True)
    is_group = models.BooleanField(default = False)
    avatar = models.ImageField(upload_to='chat_app/group_avatars/', blank = True, null = True)
    admin = models.ForeignKey(
        'user_app.User',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
        related_name = 'admin_chat'
    )
    users = models.ManyToManyField('user_app.User', related_name = 'chats')
    
    def __str__(self):
        return f'Чат {self.id}: {self.name}'
    
 

class Message(models.Model):
    text = models.TextField(blank = True, null = True)
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE, related_name = 'messages')
    created_at = models.DateTimeField(auto_now_add = True)

    sender = models.ForeignKey(
        'user_app.User', 
        on_delete = models.SET_NULL, 
        blank = True, null = True, 
        related_name = 'sent_messages'
    )
    
    readers = models.ManyToManyField(
        'user_app.User', 
        blank = True, 
        related_name = 'read_messages'
    )
    
    def __str__(self):
        return f'Повідомлення {self.id} от {self.sender}'
    

class MessageImage(models.Model):
    image = models.ImageField(upload_to='chat_app/message_images/')
    message = models.ForeignKey(Message, on_delete = models.CASCADE, related_name = 'images')
    
    def __str__(self):
        return f'Зображення до повідомлення {self.message.id}'
    