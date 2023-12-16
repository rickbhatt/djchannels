from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json
from asgiref.sync import async_to_sync
from .models import Chat, Group
from channels.db import database_sync_to_async
from django.db import IntegrityError


class ChatSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connected...")
        # print(f"event = {event}")
        print("Channel layer =", self.channel_layer)
        print("Channel name =", self.channel_name)

        # ADDINNG CHANNEL LAYER TO A GROUP
        async_to_sync(self.channel_layer.group_add)("programmers", self.channel_name)

        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        # print(f"message received from client = {event['text']}")

        client_message = event["text"]

        parsed_chat_message = json.loads(client_message)

        print(parsed_chat_message["message"])

        # self.send({"type": "websocket.send", "text": chat_message})

        """
        SENDING MESSAGE TO A GROUP SO THAT
        ALL THE CHANNELS IN THE GROUP RECEiVES
        THE MESSAGE
        """

        async_to_sync(self.channel_layer.group_send)(
            "programmers",
            {
                "type": "chat.message",  # event name
                "message": client_message,
            },
        )

    """
    the below handler is the handle the event
    named in the type. Namning convention is to replace
    the dot with an underscore in the handler
    """

    def websocket_disconnect(self, event):
        print("Websocket, Disconnect...")
        print("Channel layer =", self.channel_layer)
        print("Channel name =", self.channel_name)
        # DICARDING GROUP ON DISCONNECT
        async_to_sync(self.channel_layer.group_discard)(
            "programmers", self.channel_name
        )

        raise StopConsumer()

    def chat_message(self, event):
        print(f"event from chat_message = {event}")
        # sending message to the group
        self.send({"type": "websocket.send", "text": event["message"]})


class ChatAsyncConsumer(AsyncConsumer):

    """this is an async consumer"""

    async def websocket_connect(self, event):
        print("Websocket Connected...")
        # print(f"event = {event}")
        # print("Channel layer =", self.channel_layer)
        # print("Channel name =", self.channel_name)

        # ADDINNG STATIC GROUP NAME AND CHANNEL LAYER TO THIS GROUP
        # await self.channel_layer.group_add("programmers", self.channel_name)

        """ADDINNG DYNAMIC GROUP NAME AND CHANNEL LAYER TO THIS GROUP"""
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"].lower()

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        self.group_obj = await handle_group_name_creation(self.group_name)

        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        # print(f"message received from client = {event['text']}")

        client_message = event["text"]

        parsed_chat_message = json.loads(client_message)

        print(self.scope["user"])
        chat_obj = await handle_chat_storage(
            self.group_obj, parsed_chat_message["message"]
        )

        # self.send({"type": "websocket.send", "text": chat_message})

        """
        SENDING MESSAGE TO A GROUP SO THAT
        ALL THE CHANNELS IN THE GROUP RECEiVES
        THE MESSAGE
        """

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",  # event name
                "message": client_message,
            },
        )

    """
    the below handler is the handle the event
    named in the type. Namning convention is to replace
    the dot with an underscore in the handler
    """

    async def websocket_disconnect(self, event):
        print("Websocket, Disconnect...")
        # print("Channel layer =", self.channel_layer)
        # print("Channel name =", self.channel_name)
        # DICARDING GROUP ON DISCONNECT
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        raise StopConsumer()

    async def chat_message(self, event):
        """
        this method handles the sending of message
        to the group.
        this is same as chat.message
        """
        print(f"event from chat_message = {event}")
        # sending message to the group
        await self.send({"type": "websocket.send", "text": event["message"]})


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
def handle_chat_storage(group_obj, chat_message):
    try:
        chat_obj = Chat.objects.create(group=group_obj, content=chat_message)
    except:
        print("An exception occurred")
