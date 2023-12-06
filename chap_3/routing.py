from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/ch3/sync/", consumers.MySyncConsumer.as_asgi()),
    path("ws/ch3/async/", consumers.MyAsyncConsumer.as_asgi()),
]
