from channels.generic.websocket import AsyncWebsocketConsumer


class PhotoConsumer(AsyncWebsocketConsumer):
    users_connections = {}

    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        if user_id not in self.users_connections:
            self.users_connections[user_id] = []
        self.users_connections[user_id].append(self)
        await self.accept()
        await self.channel_layer.group_add('name', self.channel_name)
        print(len(self.users_connections))

    async def disconnect(self, code):
        user_id = self.scope['url_route']['kwargs']['user_id']
        if user_id in self.users_connections:
            self.users_connections[user_id].remove(self)

            if not self.users_connections[user_id]:
                del self.users_connections[user_id]

    @staticmethod
    async def get_channels():
        print(123123123)
        return PhotoConsumer.users_connections
