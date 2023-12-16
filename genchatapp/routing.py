from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path(
        "ws/genchatapp/async/<str:group_name>/",
        consumer.ChatGenericAsyncConsumer.as_asgi(),
    )
]
