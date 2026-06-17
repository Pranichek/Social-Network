from .models import Message, Chat

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]['kwargs']["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"
        
        self.user_pseudonym = await self.get_pseudonym(self.scope["user"])

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        await self.send(
            text_data=json.dumps({
                "action": 'connection_information',
                "message" : "Підключено успішно",
            })
        )
        print("Підключення було встановлено")
    
    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message_text = data.get("messageText", "").strip()

        if message_text:
            message_data = await self.save_message(message_text)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_chat_message",
                    "message_text": message_text,
                    "sender": self.user_pseudonym,
                    "created_at": message_data["created_at"],
                    "images": message_data.get("images", [])
                }
            )

    async def send_chat_message(self, event):
        is_me = self.user_pseudonym == event['sender']

        await self.send(text_data=json.dumps({
            'action': 'chat_message',
            'message_text': event['message_text'],
            'sender': event['sender'],
            'created_at': event['created_at'],
            'is_current_user': is_me,
            "images": event.get("images", [])
        }))

        chat_members = await self.get_chat_members_ids() 
        for member_id in chat_members:
            await self.channel_layer.group_send(
                f"user_notifications_{member_id}", 
                {
                    "type": "new_message_notification",
                    "chat_id": self.chat_id,
                    "sender": self.user_pseudonym,
                    'message_text': event['message_text']
                }
            )

    @database_sync_to_async
    def get_chat_members_ids(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return list(chat.users.values_list('id', flat=True))
        except Chat.DoesNotExist:
            return []

    @database_sync_to_async
    def save_message(self, text):
        user = self.scope["user"]
        message = Message.objects.create(chat_id=self.chat_id, sender=user, text=text)
        return {
            "created_at": timezone.localtime(message.created_at).isoformat(),
            'images': []
        }
    
    @database_sync_to_async
    def get_pseudonym(self, user):
        if user.is_authenticated:
            return user.userprofile.pseudonym
        return "Невідомий"

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f"user_notifications_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def new_message_notification(self, event):
        await self.send(text_data=json.dumps({
            "action": "new_message",
            "chat_id": event["chat_id"],
            "sender": event["sender"],
            "text": event["message_text"]
        }))

    
class OnlineStatusConsumer(AsyncWebsocketConsumer):
    online_users = set()

    async def connect(self):
        self.user = self.scope["user"]
        self.user_id = str(self.user.id)

        self.group_name = "online_users"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        self.online_users.add(self.user_id)
        # Поточний користувач отримує іфнормацію про статуси інших користувачів
        for user_id in self.online_users:
            await self.send_status(user_id, "online")

        # Поточний користувач надсилає іфнормацію про свій статус іншим користувачам
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "online_status",
                "user_id": self.user_id,
                "status": "online"
            }
        )

    async def disconnect(self, code):
        self.online_users.discard(self.user_id)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "online_status",
                "user_id": self.user_id,
                "status": "offline"
            }
        )

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # для відображення в хедері чату статус 
    # classmethod - щоб можна було звертатися до методів класу, без створення екземплрів
    @classmethod
    def is_online(cls, user_id):
        return str(user_id) in cls.online_users
    
    @classmethod
    def get_online_count(cls, user_ids):
        return sum(1 for user_id in user_ids if str(user_id) in cls.online_users)

    async def online_status(self, event):
        await self.send_status(event["user_id"], event["status"])

    async def send_status(self, user_id, status):
        await self.send(text_data=json.dumps({
            "user_id": user_id,
            "status": status
        }))
