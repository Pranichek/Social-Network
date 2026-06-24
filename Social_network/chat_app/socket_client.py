import asyncio
import socketio
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async

from django.conf import settings

all_online_users: set = set()

def cloudinary_url_from_field(image_field):
    name = getattr(image_field, "name", "") or str(image_field)
    if not name:
        return ""
    if name.startswith("http://") or name.startswith("https://"):
        return name
    cloud_name = settings.CLOUDINARY_STORAGE.get("CLOUD_NAME", "depqshccq")
    return f"https://res.cloudinary.com/{cloud_name}/image/upload/{name}"

sio = socketio.AsyncClient(logger=True, engineio_logger=True)


EXPRESS_URL = "https://unreprimanded-unavidly-margene.ngrok-free.dev"


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


@sio.event(namespace="/django-bridge")
async def connect():
    from .consumers import OnlineStatusConsumer
    print("Django підключився до Express")

    online = set(OnlineStatusConsumer.online_users) | all_online_users

    await sio.emit("django_event", {
        "type": "sync",
        "onlineUsers": [int(u) for u in online]
    }, namespace="/django-bridge")

@sio.event(namespace="/django-bridge")
async def disconnect():
    print("Django відключився від Express")


@sio.on("server_event", namespace="/django-bridge")
async def on_server_event(data):
    print("Подія від Express:", data)

    event_type = data.get("type")
    channel_layer = get_channel_layer()

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
        print("Отримали від Express повний список онлайн:", ids)
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
                    f"unread_{member_id}",
                    {
                        "type": "unread_update"
                    }
                )
        return
    if event_type == "friend:request":
        to_user_id = data.get("toUserId")
        from_user_id = data.get("fromUserId")
        pseudonym = data.get("pseudonym", "")
        username = data.get("username", "")

        if to_user_id:
            await channel_layer.group_send(
                f"friend_request_{to_user_id}",
                {
                    "type": "friend_request_update",
                    "from_user_id": from_user_id,
                    "pseudonym": pseudonym,
                    "username": username,
                }
            )
        return

def start_socket_client():
    global background_loop
    background_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(background_loop)

    async def start():
        await sio.connect(EXPRESS_URL, namespaces=["/django-bridge"])
        await sio.wait()

    background_loop.run_until_complete(start())