from django import forms
from service_objects.services import Service

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ChangePhotoService(Service):
    photo_id = forms.IntegerField(required=True)
    user_id = forms.IntegerField(required=True)
    title = forms.CharField(required=True)
    status = forms.CharField(required=True)

    def process(self):
        if self.is_valid():
            self.send_message()

    def send_message(self):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{self.cleaned_data["user_id"]}',
            {
                'type': 'status_change',
                'message': 'Status changed',
                'photo_id': self.cleaned_data['photo_id'],
                'title': self.cleaned_data['title'],
                'status': self.cleaned_data['status'],
            }
        )
