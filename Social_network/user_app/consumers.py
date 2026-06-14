# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.core.cache import cache
# from asgiref.sync import sync_to_async

# class UserStatusConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
#         if self.user.is_authenticated:
#             await self.channel_layer.group_add('global_online_status', self.channel_name) 
#             await self.set_online_status(self.user.id, True)
#             await self.channel_layer.group_send('global_online_status', {
#                 'type': 'status_update',
#                 'user_id': self.user.id,
#                 'status': 'online'
#             })

#             await self.accept()
#         else:
#             await self.close()

#     async def disconnect(self, close_code):
#         if self.user.is_authenticated:
#             await self.channel_layer.group_discard('global_online_status', self.channel_name)
#             await self.set_online_status(self.user.id, False)
#             await self.channel_layer.group_send('global_online_status', {
#                 'type': 'status_update',
#                 'user_id': self.user.id,
#                 'status': 'offline'
#             })
    
#     async def status_update(self, event):
#         await self.send(text_data=json.dumps({
#             'action': 'status_update',
#             'user_id': event['user_id'],
#             'status': event['status']
#         }))

#     @sync_to_async
#     def set_online_status(self, user_id, is_online):
#         cache_key = f'user_online_{user_id}'
#         if is_online:
#             cache.set(cache_key, True, timeout=300)
#         else:
#             cache.delete(cache_key)
