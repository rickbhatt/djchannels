from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/chatapp/sync/<str:group_name>/", consumers.ChatSyncConsumer.as_asgi()),
    path("ws/chatapp/async/<str:group_name>/", consumers.ChatAsyncConsumer.as_asgi()),
]
