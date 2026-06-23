from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

from .models import Friendship


class FriendRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = None

        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.group_name = f'friend_request_{self.user.id}'
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        )
        await self.accept()
        await self.send_count()

    async def disconnect(self, code):
        if hasattr(self, "group_name") and self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def friend_request_update(self, event):
        await self.send_count()
        
    async def send_count(self):
        count = await self.get_pending_count()
        await self.send(text_data = json.dumps({
            'count': count
        }))

    @database_sync_to_async
    def get_pending_count(self):
        return Friendship.objects.filter(
            to_user = self.user,
            status = "pending",
        ).count()