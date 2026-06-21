# from .models import Message, Chat

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.utils import timezone
# from .socket_client import sio, background_loop
# import asyncio


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.chat_id = self.scope["url_route"]['kwargs']["chat_id"]
#         self.room_group_name = f"chat_{self.chat_id}"
        
#         self.user_pseudonym = await self.get_pseudonym(self.scope["user"])

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#         await self.accept()
#         await self.send(
#             text_data=json.dumps({
#                 "action": 'connection_information',
#                 "message" : "Підключено успішно",
#             })
#         )
    
#     # async def receive(self, text_data=None):
#     #     data = json.loads(text_data)
#     #     message_text = data.get("messageText", "").strip()

#     #     if message_text:
#     #         message_data = await self.save_message(message_text)

#     #         await self.channel_layer.group_send(
#     #             self.room_group_name,
#     #             {
#     #                 "type": "send_chat_message",
#     #                 "message_text": message_text,
#     #                 "sender": self.user_pseudonym,
#     #                 "created_at": message_data["created_at"],
#     #                 "images": message_data.get("images", [])
#     #             }
#     #         )

#     async def receive(self, text_data=None):
#         data = json.loads(text_data)
#         message_text = data.get("messageText", "").strip()

#         print("zashlo")

#         if message_text:
#             message_data = await self.save_message(message_text)

#             # Локальный broadcast внутри Django (для веб-клиентов)
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "send_chat_message",
#                     "message_text": message_text,
#                     "sender": self.user_pseudonym,
#                     "created_at": message_data["created_at"],
#                     "images": message_data.get("images", [])
#                 }
#             )

#             # Дублирование события в Express через фоновый event loop
#             if sio.connected and background_loop:
#                 # Превращаем datetime в строку во избежание ошибок сериализации JSON
#                 date_str = message_data["created_at"]
#                 if hasattr(date_str, 'isoformat'):
#                     date_str = date_str.isoformat()
#                 else:
#                     date_str = str(date_str)

#                 payload = {
#                     "type": "message:new",
#                     "chatId": str(self.chat_id),
#                     "message": {
#                         "text": message_text,
#                         "sender": self.user_pseudonym,
#                         "created_at": date_str,
#                         "images": message_data.get("images", [])
#                     }
#                 }
                
#                 future = asyncio.run_coroutine_threadsafe(
#                     sio.emit("django_event", payload, namespace="/django-bridge"),
#                     background_loop
#                 )
                
#                 try:
#                     await asyncio.wrap_future(future)
#                 except Exception as e:
#                     print(f"⚠️ Ошибка дублирования в Express: {e}")

    
#     async def send_chat_message(self, event):
#         print(f"DEBUG: Пытаюсь отправить в браузер: {event}")
#         is_me = self.user_pseudonym == event['sender']

#         await self.send(text_data=json.dumps({
#             'action': 'chat_message',
#             'message_text': event['message_text'],
#             'sender': event['sender'],
#             'created_at': event['created_at'],
#             'is_current_user': is_me,
#             "images": event.get("images", [])
#         }))

#         if is_me:
#             chat_members = await self.get_chat_members_ids()
#             for member_id in chat_members:
#                 if member_id != self.scope["user"].id: 
#                     await self.channel_layer.group_send(
#                         f"user_notifications_{member_id}",
#                         {
#                             "type": "new_message_notification",
#                             "chat_id": self.chat_id,
#                             "sender": self.user_pseudonym,
#                             "message_text": event['message_text'],
#                             'created_at': event['created_at'],
#                         }
#                     )

    

#     @database_sync_to_async
#     def get_chat_members_ids(self):
#         try:
#             chat = Chat.objects.get(id=self.chat_id)
#             return list(chat.users.values_list('id', flat=True))
#         except Chat.DoesNotExist:
#             return []

#     @database_sync_to_async
#     def save_message(self, text):
#         user = self.scope["user"]
#         message = Message.objects.create(chat_id=self.chat_id, sender=user, text=text)
#         return {
#             "created_at": timezone.localtime(message.created_at).isoformat(),
#             'images': []
#         }
    
#     @database_sync_to_async
#     def get_pseudonym(self, user):
#         if user.is_authenticated:
#             return user.userprofile.pseudonym
#         return "Невідомий"

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         if not self.user.is_authenticated:
#             await self.close()
#             return
        
#         self.group_name = f"user_notifications_{self.user.id}"
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def new_message_notification(self, event):
#         await self.send(text_data=json.dumps({
#             "action": "new_message_notification",
#             "chat_id": event["chat_id"],
#             "sender": event["sender"],
#             "message_text": event["message_text"],
#             "created_at": event['created_at']
#         }))

    
# class OnlineStatusConsumer(AsyncWebsocketConsumer):
#     online_users = set()

#     async def connect(self):
#         self.user = self.scope["user"]
#         self.user_id = str(self.user.id)

#         self.group_name = "online_users"
#         await self.channel_layer.group_add(self.group_name, self.channel_name)

#         await self.accept()
#         self.online_users.add(self.user_id)
#         for user_id in self.online_users:
#             await self.send_status(user_id, "online")

#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "online_status",
#                 "user_id": self.user_id,
#                 "status": "online"
#             }
#         )

#     async def disconnect(self, code):
#         self.online_users.discard(self.user_id)
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "online_status",
#                 "user_id": self.user_id,
#                 "status": "offline"
#             }
#         )

#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     # для відображення в хедері чату статус 
#     # classmethod - щоб можна було звертатися до методів класу, без створення екземплрів
#     @classmethod
#     def is_online(cls, user_id):
#         return str(user_id) in cls.online_users
    
#     @classmethod
#     def get_online_count(cls, user_ids):
#         return sum(1 for user_id in user_ids if str(user_id) in cls.online_users)

#     async def online_status(self, event):
#         await self.send_status(event["user_id"], event["status"])

#     async def send_status(self, user_id, status):
#         await self.send(text_data=json.dumps({
#             "user_id": user_id,
#             "status": status
#         }))


# import json
# import asyncio
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.utils import timezone
# from .models import Message, Chat
# from .socket_client import sio, background_loop

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
        
#         if not self.user.is_authenticated:
#             await self.close()
#             return
        
#         self.user_id = str(self.user.id)
#         self.group_name = "online_users"

#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#         self.online_users.add(self.user_id)

#         if background_loop:
#             asyncio.run_coroutine_threadsafe(
#                 sio.emit("django_event", {"type": "user:online", "userId": int(self.user_id)}, namespace="/django-bridge"),
#                 background_loop
#             )

#         for user_id in self.online_users:
#             await self.send_status(user_id, "online")

#         await self.channel_layer.group_send(
#             self.group_name,
#             {"type": "online_status", "user_id": self.user_id, "status": "online"}
#         )

#     async def receive(self, text_data=None):
#         data = json.loads(text_data)
#         message_text = data.get("messageText", "").strip()

#         if message_text:
#             message_data = await self.save_message(message_text)

#             # Локальный broadcast внутри Django
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "send_chat_message",
#                     "message_text": message_text,
#                     "sender": self.user_pseudonym,
#                     "created_at": message_data["created_at"],
#                     "images": message_data.get("images", [])
#                 }
#             )

#             if background_loop: 
#                 date_str = message_data["created_at"]
#                 if hasattr(date_str, 'isoformat'):
#                     date_str = date_str.isoformat()
#                 else:
#                     date_str = str(date_str)

#                 payload = {
#                     "type": "message:new",
#                     "chatId": str(self.chat_id),
#                     "message": {
#                         "text": message_text,
#                         "sender": self.user_pseudonym,
#                         "created_at": date_str,
#                         "images": message_data.get("images", [])
#                     }
#                 }

#                 future = asyncio.run_coroutine_threadsafe(
#                     sio.emit("django_event", payload, namespace="/django-bridge"),
#                     background_loop
#                 )
#                 try:
#                     await asyncio.wrap_future(future)
#                     print("✅ Сообщение отправлено в Express")
#                 except Exception as e:
#                     print(f"⚠️ Ошибка дублирования в Express: {e}")

#     async def send_chat_message(self, event):
#         is_me = self.user_pseudonym == event['sender']
#         await self.send(text_data=json.dumps({
#             'action': 'chat_message',
#             'message_text': event['message_text'],
#             'sender': event['sender'],
#             'created_at': event['created_at'],
#             'is_current_user': is_me,
#             "images": event.get("images", [])
#         }))

#         if is_me:
#             chat_members = await self.get_chat_members_ids()
#             for member_id in chat_members:
#                 if member_id != self.scope["user"].id:
#                     await self.channel_layer.group_send(
#                         f"user_notifications_{member_id}",
#                         {
#                             "type": "new_message_notification",
#                             "chat_id": self.chat_id,
#                             "sender": self.user_pseudonym,
#                             "message_text": event['message_text'],
#                             'created_at': event['created_at'],
#                         }
#                     )

#     @database_sync_to_async
#     def get_chat_members_ids(self):
#         try:
#             chat = Chat.objects.get(id=self.chat_id)
#             return list(chat.users.values_list('id', flat=True))
#         except Chat.DoesNotExist:
#             return []

#     @database_sync_to_async
#     def save_message(self, text):
#         user = self.scope["user"]
#         message = Message.objects.create(chat_id=self.chat_id, sender=user, text=text)
#         return {
#             "created_at": timezone.localtime(message.created_at).isoformat(),
#             'images': []
#         }

#     @database_sync_to_async
#     def get_pseudonym(self, user):
#         if user.is_authenticated:
#             return user.userprofile.pseudonym
#         return "Невідомий"


# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         if not self.user.is_authenticated:
#             await self.close()
#             return

#         self.group_name = f"user_notifications_{self.user.id}"
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def new_message_notification(self, event):
#         await self.send(text_data=json.dumps({
#             "action": "new_message_notification",
#             "chat_id": event["chat_id"],
#             "sender": event["sender"],
#             "message_text": event["message_text"],
#             "created_at": event['created_at']
#         }))
# class OnlineStatusConsumer(AsyncWebsocketConsumer):
#     online_users = set()  

#     async def connect(self):
#         self.user = self.scope["user"]
#         self.user_id = str(self.user.id)
#         self.group_name = "online_users"

#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#         self.online_users.add(self.user_id)

#         if background_loop:
#             asyncio.run_coroutine_threadsafe(
#                 sio.emit("django_event", {"type": "user:online", "userId": int(self.user_id)}, namespace="/django-bridge"),
#                 background_loop
#             )


#         for user_id in self.online_users:
#             await self.send_status(user_id, "online")

#         await self.channel_layer.group_send(
#             self.group_name,
#             {"type": "online_status", "user_id": self.user_id, "status": "online"}
#         )

#     async def disconnect(self, code):
#         self.online_users.discard(self.user_id)

#         if background_loop:
#             asyncio.run_coroutine_threadsafe(
#                 sio.emit("django_event", {"type": "user:offline", "userId": int(self.user_id)}, namespace="/django-bridge"),
#                 background_loop
#             )

#         await self.channel_layer.group_send(
#             self.group_name,
#             {"type": "online_status", "user_id": self.user_id, "status": "offline"}
#         )
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     @classmethod
#     def is_online(cls, user_id):
#         return str(user_id) in cls.online_users

#     @classmethod
#     def get_online_count(cls, user_ids):
#         return sum(1 for user_id in user_ids if str(user_id) in cls.online_users)

#     async def online_status(self, event):
#         await self.send_status(event["user_id"], event["status"])

#     async def send_status(self, user_id, status):
#         await self.send(text_data=json.dumps({
#             "user_id": user_id,
#             "status": status
#         }))


# class OnlineStatusConsumer(AsyncWebsocketConsumer):
#     online_users = set()

#     async def connect(self):
#         self.user = self.scope["user"]
#         self.user_id = str(self.user.id)
#         self.group_name = "online_users"

#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#         self.online_users.add(self.user_id)

#         if sio.connected and background_loop:
#             asyncio.run_coroutine_threadsafe(
#                 sio.emit("django_event", {"type": "user:online", "userId": int(self.user_id)}, namespace="/django-bridge"),
#                 background_loop
#             )

#         for user_id in self.online_users:
#             await self.send_status(user_id, "online")

#         await self.channel_layer.group_send(
#             self.group_name,
#             {"type": "online_status", "user_id": self.user_id, "status": "online"}
#         )

#     async def disconnect(self, code):
#         self.online_users.discard(self.user_id)

#         if sio.connected and background_loop:
#             asyncio.run_coroutine_threadsafe(
#                 sio.emit("django_event", {"type": "user:offline", "userId": int(self.user_id)}, namespace="/django-bridge"),
#                 background_loop
#             )

#         await self.channel_layer.group_send(
#             self.group_name,
#             {"type": "online_status", "user_id": self.user_id, "status": "offline"}
#         )
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     @classmethod
#     def is_online(cls, user_id):
#         return str(user_id) in cls.online_users

#     @classmethod
#     def get_online_count(cls, user_ids):
#         return sum(1 for user_id in user_ids if str(user_id) in cls.online_users)

#     async def online_status(self, event):
#         await self.send_status(event["user_id"], event["status"])

#     async def send_status(self, user_id, status):
#         await self.send(text_data=json.dumps({
#             "user_id": user_id,
#             "status": status
#         }))

from .socket_client import all_online_users
from .models import Message, Chat
from .socket_client import sio, background_loop
from .socket_client import cloudinary_url_from_field

import json
import asyncio
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

        await self.send(text_data=json.dumps({
            "action": 'connection_information',
            "message": "Підключено успішно",
        }))

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        action = data.get("action", "")

        if action == "send_message":
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
                        "images": message_data.get("images", []),
                    }
                )

                if background_loop:
                    date_str = message_data["created_at"]
                    if hasattr(date_str, 'isoformat'):
                        date_str = date_str.isoformat()
                    else:
                        date_str = str(date_str)

                    payload = {
                        "type": "message:new",
                        "chatId": str(self.chat_id),
                        "message": {
                            "text": message_text,
                            "sender": self.user_pseudonym,
                            "created_at": date_str,
                            "images": message_data.get("images", []),
                        }
                    }

                    asyncio.run_coroutine_threadsafe(
                        sio.emit("django_event", payload, namespace="/django-bridge"),
                        background_loop
                    )

        elif action == "mark_read":
            pass

    async def send_chat_message(self, event):
        is_me = self.user_pseudonym == event['sender']
        
        images = event.get("images", [])
        message_id = event.get("message_id")
        
        if not images and message_id:
            images = await self.get_message_images(message_id)
        
        await self.send(text_data=json.dumps({
            'action': 'chat_message',
            'message_text': event['message_text'],
            'sender': event['sender'],
            'created_at': event['created_at'],
            'is_current_user': is_me,
            "images": images,
            "message_id": message_id
        }))

        if is_me:
            chat_info = await self.get_chat_info()
            chat_members = await self.get_chat_members_ids()

            for member_id in chat_members:
                
                await self.channel_layer.group_send(
                    f"user_notifications_{member_id}",
                    {
                        "type": "chat_card_update",
                        "chat_id": self.chat_id,
                        "is_group": chat_info["is_group"],
                        "chat_members": chat_members,
                        "sender": event['sender'],
                        "sender_id": self.scope["user"].id,
                        "message_text": event['message_text'],
                        "created_at": event['created_at'],
                    }
                )

                if member_id != self.scope["user"].id:
                    await self.channel_layer.group_send(
                        f"user_notifications_{member_id}",
                        {
                            "type": "new_message_notification",
                            "chat_id": self.chat_id,
                            "sender": event['sender'],
                            "message_text": event['message_text'],
                            'created_at': event['created_at'],
                        }
                    )

    # Добавить новый метод:
    # @database_sync_to_async
    # def get_message_images(self, message_id):
    #     try:
    #         message = Message.objects.prefetch_related('images').get(id=message_id)
    #         return [img.image.url for img in message.images.all()]
    #     except Message.DoesNotExist:
    #         return []

    @database_sync_to_async
    def get_chat_info(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return {"is_group": chat.is_group}
        except Chat.DoesNotExist:
            return {"is_group": False}
        
    @database_sync_to_async
    def get_message_images(self, message_id):
        try:
            message = Message.objects.prefetch_related('images').get(id=message_id)
            return [cloudinary_url_from_field(img.image) for img in message.images.all()]
        except Message.DoesNotExist:
            return []

    @database_sync_to_async
    def get_chat_members_ids(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return list(chat.users.values_list('id', flat=True))
        except Chat.DoesNotExist:
            return []

    # @database_sync_to_async
    # def save_message(self, text):
    #     user = self.scope["user"]
    #     message = Message.objects.create(chat_id=self.chat_id, sender=user, text=text)
    #     return {
    #         "created_at": timezone.localtime(message.created_at).isoformat(),
    #         'images': []
    #     }
    
    @database_sync_to_async
    def save_message(self, text, images=None):
        from .models import MessageImage
        user = self.scope["user"]
        message = Message.objects.create(chat_id=self.chat_id, sender=user, text=text)
        
        image_urls = []
        if images:
            for img_url in images:
                MessageImage.objects.create(message=message, image=img_url)
                image_urls.append(img_url)
        
        return {
            "id": message.id,
            "created_at": timezone.localtime(message.created_at).isoformat(),
            'images': image_urls
        }

    @database_sync_to_async
    def get_pseudonym(self, user):
        if user.is_authenticated:
            return user.userprofile.pseudonym
        return "Невідомий"


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_notifications_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def chat_card_update(self, event):
        await self.send(text_data=json.dumps({
            "action": "chat_card_update",
            "chat_id": event["chat_id"],
            "is_group": event["is_group"],
            "chat_members": event["chat_members"],
            "sender": event["sender"],
            "sender_id": event["sender_id"],
            "message_text": event["message_text"],
            "created_at": event["created_at"],
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def new_message_notification(self, event):
        await self.send(text_data=json.dumps({
            "action": "new_message_notification",
            "chat_id": event["chat_id"],
            "sender": event["sender"],
            "message_text": event["message_text"],
            "created_at": event['created_at']
        }))


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    online_users = set()

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.user_id = str(self.user.id)
        self.group_name = "online_users"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        self.online_users.add(self.user_id)

        if background_loop:
            asyncio.run_coroutine_threadsafe(
                sio.emit(
                    "django_event",
                    {"type": "user:online", "userId": int(self.user_id)},
                    namespace="/django-bridge"
                ),
                background_loop
            )

        from .socket_client import all_online_users
        all_online = self.online_users | all_online_users

        for user_id in all_online:
            await self.send_status(user_id, "online")

        await self.channel_layer.group_send(
            self.group_name,
            {"type": "online_status", "user_id": self.user_id, "status": "online"}
        )

    async def disconnect(self, code):
        self.online_users.discard(self.user_id)

        if background_loop:
            asyncio.run_coroutine_threadsafe(
                sio.emit("django_event", {"type": "user:offline", "userId": int(self.user_id)}, namespace="/django-bridge"),
                background_loop
            )

        await self.channel_layer.group_send(
            self.group_name,
            {"type": "online_status", "user_id": self.user_id, "status": "offline"}
        )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

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