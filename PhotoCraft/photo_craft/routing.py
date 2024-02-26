from django.urls import re_path
from core_api import consumers

websocket_urlpatterns = [
    re_path(r'ws/change_status/$', consumers.PhotoConsumer.as_asgi()),
]
