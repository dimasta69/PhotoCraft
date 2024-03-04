import asyncio

from service_objects.services import Service
import json

from websocket_app.consumers import PhotoConsumer
from django import forms


class StatusService(Service):
    user_id = forms.IntegerField()
    id = forms.IntegerField()
    status = forms.CharField()

    def process(self):
        if self.is_valid():
            user_id = self.cleaned_data['user_id']
            channels = self.get_channels()
            print(len(channels))
            if user_id in channels:
                message = {
                    'name': {
                        'photo_id': self.cleaned_data['id'],
                        'status': self.cleaned_data['status']
                    }
                }
                for connection in channels[user_id]:
                    connection.send(json.dumps(message))

    def get_channels(self):
        return asyncio.run(PhotoConsumer.get_channels())
