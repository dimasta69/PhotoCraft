from channels.generic.websocket import AsyncWebsocketConsumer
import json


class PhotoConsumer(AsyncWebsocketConsumer):
    users_connections = {}
    group_name = 'name'

    async def connect(self):
        user_id = self.scope['user'].id
        if user_id not in self.users_connections:
            self.users_connections[user_id] = []
        self.users_connections[user_id].append(self)
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.change_status({
            'user_id': user_id,
            'id': None,
            'status': 'connected'
        })

    async def disconnect(self, code):
        user_id = self.scope['user'].id

        if user_id in self.users_connections:
            self.users_connections[user_id].remove(self)

            if not self.users_connections[user_id]:
                del self.users_connections[user_id]

    async def change_status(self, event):
        user_id = event['user_id']
        photo_id = event['id']
        status = event['status']
        print(123)
        print(status)

        if user_id in self.users_connections:
            for connection in self.users_connections[user_id]:
                await connection.send(json.dumps({'photo_id': photo_id, 'status': status}))
