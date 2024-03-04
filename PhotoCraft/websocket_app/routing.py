from django.urls import re_path
from websocket_app import consumers

websocket_urlpatterns = [
    re_path(r'ws/change_status/(?P<user_id>\d+)/$', consumers.PhotoConsumer.as_asgi()),
]
