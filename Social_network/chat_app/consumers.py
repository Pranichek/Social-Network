import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]['kwargs']["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        await self.send(
            # dumps - Приобразовывает из словаря в строку 
            text_data=json.dumps({"message" : "Підключено успішно"})
        )
        print("Підключення було встановлено")