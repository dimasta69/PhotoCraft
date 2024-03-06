from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.layers import get_channel_layer


class PhotoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'user_{self.user_id}'
        self.all_users_group_name = 'all_users'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.all_users_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            f'user_{self.user_id}',
            {
                'type': 'status_change',
                'message': 'message',
                'photo_id': 1,
                'title': 'test',
                'status': 'test',
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def status_change(self, event):
        message = event['message']
        photo_id = event['photo_id']
        title = event['title']
        status = event['status']
        await self.send(text_data=json.dumps({
            'photo_id': photo_id,
            'title': title,
            'message': message,
            'status': status,
        }))
