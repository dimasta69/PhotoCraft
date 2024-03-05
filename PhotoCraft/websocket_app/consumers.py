from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PhotoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'user_{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            'user_1',
            {
                'type': 'status_change',
                'message': 'Статус был изменен'
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(123)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'status_change',
                'message': message
            }
        )

    async def status_change(self, event):
        message = event['message']
        print(456)

        await self.send(text_data=json.dumps({
            'message': message
        }))
