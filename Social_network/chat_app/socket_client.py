import asyncio
import os
import socketio
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async

from django.conf import settings

all_online_users: set = set()

def cloudinary_url_from_field(image_field) -> str:
    name = getattr(image_field, "name", "") or str(image_field)
    if not name:
        return ""
    if name.startswith("http://") or name.startswith("https://"):
        return name
    cloud_name = settings.CLOUDINARY_STORAGE.get("CLOUD_NAME", "depqshccq")
    return f"https://res.cloudinary.com/{cloud_name}/image/upload/{name}"

sio = socketio.AsyncClient(logger=True, engineio_logger=True)
# EXPRESS_URL = "https://unreprimanded-unavidly-margene.ngrok-free.dev"

EXPRESS_URL = os.environ.get("EXPRESS_URL", "")


background_loop = None


@database_sync_to_async
def get_chat_members_ids(chat_id):
    from .models import Chat
    try:
        chat = Chat.objects.get(id=chat_id)
        return list(chat.users.values_list('id', flat=True))
    except Chat.DoesNotExist:
        return []


@database_sync_to_async
def get_message_images_by_id(message_id):
    from .models import Message
    try:
        message = Message.objects.prefetch_related('images').get(id=message_id)
        return [cloudinary_url_from_field(img.image) for img in message.images.all()]
    except Message.DoesNotExist:
        return []


# @sio.event(namespace="/django-bridge")
# async def connect():
#     from .consumers import OnlineStatusConsumer
#     print("✅ Django підключився до Express")
#     print("Online users at connect:", OnlineStatusConsumer.online_users)

#     # Отправляем Express всех онлайн-юзеров Django
#     for user_id in OnlineStatusConsumer.online_users:
#         await sio.emit("django_event", {
#             "type": "user:online",
#             "userId": int(user_id)
#         }, namespace="/django-bridge")

#     # Запрашиваем у Express его онлайн-юзеров
#     await sio.emit("django_event", {
#         "type": "users:request_online"
#     }, namespace="/django-bridge")

@sio.event(namespace="/django-bridge")
async def connect():
    from .consumers import OnlineStatusConsumer
    print("✅ Django підключився до Express")

    online = set(OnlineStatusConsumer.online_users) | all_online_users
    print("Відправляємо Express повний список онлайн:", online)

    await sio.emit("django_event", {
        "type": "sync",
        "onlineUsers": [int(u) for u in online]
    }, namespace="/django-bridge")

@sio.event(namespace="/django-bridge")
async def disconnect():
    print("❌ Django відключився від Express")


@sio.on("server_event", namespace="/django-bridge")
async def on_server_event(data):
    print("📨 Подія від Express:", data)

    event_type = data.get("type")
    channel_layer = get_channel_layer()

    # Express запросил список онлайн-юзеров Django
    if event_type == "users:request_online":
        from .consumers import OnlineStatusConsumer
        online = set(OnlineStatusConsumer.online_users)
        print("Express запросил онлайн-юзеров, отправляем:", online)
        for user_id in online:
            await sio.emit("django_event", {
                "type": "user:online",
                "userId": int(user_id)
            }, namespace="/django-bridge")
        return

    # Express сообщает что юзер онлайн
    if event_type == "user:online":
        user_id = data.get("userId") or data.get("id")
        if user_id:
            all_online_users.add(str(user_id))
            await channel_layer.group_send(
                "online_users",
                {"type": "online_status", "user_id": str(user_id), "status": "online"}
            )
        return
    
    if event_type == "sync":
        ids = data.get("onlineUsers", [])
        print("📥 Отримали від Express повний список онлайн:", ids)
        channel_layer = get_channel_layer()
        for uid in ids:
            suid = str(uid)
            if suid not in all_online_users:
                all_online_users.add(suid)
                await channel_layer.group_send(
                    "online_users",
                    {"type": "online_status", "user_id": suid, "status": "online"}
                )
        return

    # Express сообщает что юзер оффлайн
    if event_type == "user:offline":
        user_id = data.get("userId") or data.get("id")
        if user_id:
            from .consumers import OnlineStatusConsumer
            OnlineStatusConsumer.online_users.discard(str(user_id))
            all_online_users.discard(str(user_id))
            await channel_layer.group_send(
                "online_users",
                {"type": "online_status", "user_id": str(user_id), "status": "offline"}
            )
        return

    # Новое сообщение от Express
    if event_type == "message:new":
        chat_id = data.get("chatId")
        message_data = data.get("message", {})
        message_id = message_data.get("id")

        if chat_id:
            raw_images = message_data.get("images", [])

            images = []
            for img in raw_images:
                if isinstance(img, dict):
                    images.append(img.get("image", ""))
                elif isinstance(img, str):
                    images.append(img)

            if not images and message_id:
                images = await get_message_images_by_id(message_id)

            sender_data = message_data.get("sender", {})
            sender_pseudonym = (
                sender_data.get("profile", {}).get("pseudonym")
                or sender_data.get("username", "Невідомий")
            ) if isinstance(sender_data, dict) else str(sender_data)

            await channel_layer.group_send(
                f"chat_{chat_id}",
                {
                    "type": "send_chat_message",
                    "message_id": message_id,
                    "message_text": message_data.get("text", ""),
                    "sender": sender_pseudonym,
                    "created_at": message_data.get("created_at"),
                    "images": images,
                }
            )

            member_ids = await get_chat_members_ids(chat_id)
            for member_id in member_ids:
                await channel_layer.group_send(
                    f"user_notifications_{member_id}",
                    {
                        "type": "new_message_notification",
                        "chat_id": chat_id,
                        "sender": sender_pseudonym,
                        "message_text": message_data.get("text", ""),
                        "created_at": message_data.get("created_at"),
                    }
                )


def start_socket_client():
    global background_loop

    if not EXPRESS_URL:
        print("⚠️ EXPRESS_URL is not configured, socket client will not start.")
        return

    background_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(background_loop)

    async def start():
        try:
            await sio.connect(EXPRESS_URL, namespaces=["/django-bridge"])
            await sio.wait()
        except socketio.exceptions.ConnectionError as exc:
            print(f"❌ Socket client connection failed: {exc}")
        except Exception as exc:
            print(f"❌ Socket client error: {exc}")

    background_loop.run_until_complete(start())