from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/ch2/sync/", consumers.MySyncConsumer.as_asgi()),
    path("ws/ch2/async/", consumers.MyAsyncConsumer.as_asgi()),
]
