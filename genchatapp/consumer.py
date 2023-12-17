from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json
from asgiref.sync import async_to_sync
from chatapp.models import Chat, Group
from channels.db import database_sync_to_async
from django.db import IntegrityError


class ChatGenericAsyncConsumer(AsyncWebsocketConsumer):

    """this is an async consumer"""

    async def connect(self):
        self.user = self.scope["user"]

        self.group_name = self.scope["url_route"]["kwargs"]["group_name"].lower()

        if self.user.is_authenticated:
            print("authentication successful connection accepted")

            self.group_obj = await handle_group_name_creation(self.group_name)

            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.channel_layer.group_add(
                self.user.user_name, self.channel_name
            )  # for sending individual messages by the admin

            await self.accept()
        else:
            print("authentication unsuccessful connection closed")
            await self.close(code=4123)

    async def receive(self, text_data=None, bytes_data=None):
        client_data = json.loads(text_data)
        client_message = client_data["message"]

        client_data["user"] = self.user.user_name

        if self.user.is_authenticated:
            chat_obj = await handle_chat_storage(
                self.group_obj, client_message, self.user
            )

            await self.channel_layer.group_send(
                self.group_name,
                {"type": "chat.message", "data": json.dumps(client_data)},
            )

        else:
            await self.send(text_data="Login required")

    async def disconnect(self, code):
        await self.close(code=4123)

    # this is the event handler of 'chat.message'
    async def chat_message(self, event):
        """
        this method handles the sending of message
        to the group.
        this is same as chat.message
        """
        # sending message to the group
        await self.send(text_data=event["data"])


@database_sync_to_async
def handle_group_name_creation(group_name):
    try:
        group_obj, created = Group.objects.get_or_create(name=group_name)
        return group_obj
    except IntegrityError as e:
        # print("Integrity error")

        pass

    except Exception as e:
        print(e)


@database_sync_to_async
def handle_chat_storage(group_obj, chat_message, user):
    try:
        chat_obj = Chat.objects.create(group=group_obj, message=chat_message, user=user)
    except Exception as e:
        print(e)
        print("An exception occurred")
