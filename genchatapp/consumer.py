from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json
from asgiref.sync import async_to_sync
from chatapp.models import Chat, Group
from channels.db import database_sync_to_async
from django.db import IntegrityError
from pprint import pprint
from channels.exceptions import StopConsumer


class ChatGenericAsyncConsumer(AsyncWebsocketConsumer):

    """this is an async consumer"""

    async def connect(self):
        try:
            self.user = self.scope["user"]

            self.group_name = self.scope["url_route"]["kwargs"]["group_name"].lower()

            if self.user.is_authenticated:
                print(
                    # f"authentication successful connection accepted {self.user.user_name}"
                )

                # pprint(self.scope)

                self.group_obj = await handle_group_name_creation(self.group_name)

                await self.channel_layer.group_add(self.group_name, self.channel_name)
                await self.channel_layer.group_add(
                    self.user.user_name, self.channel_name
                )  # for sending individual messages by the admin

                await self.accept()

                await self.send_initial_messages()

            else:
                # print("authentication unsuccessful connection closed")
                await self.close(code=4173)
        except Exception as e:
            print(f"exception in connect = {e}")

    async def receive(self, text_data=None, bytes_data=None):
        client_data = json.loads(text_data)
        client_message = client_data["message"]

        try:
            if self.user.is_authenticated:
                client_data["user"] = self.user.user_name
                chat_obj = await handle_chat_storage(
                    self.group_obj, client_message, self.user
                )

                await self.channel_layer.group_send(
                    self.group_name,
                    {"type": "chat.message", "data": json.dumps(client_data)},
                )

            else:
                await self.send(text_data="Login required")

                await self.close(code=4173)
        except Exception as e:
            print(f"exception in receive = {e}")

    async def disconnect(self, code):
        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            if self.user.is_authenticated:
                await self.channel_layer.group_discard(
                    self.user.user_name, self.channel_name
                )  # for sending individual messages by the admin
        except Exception as e:
            print(f"exception in disconnect = {e}")

        await self.close(code=4123)
        raise StopConsumer()

    async def send_initial_messages(self):
        # Your logic to send initial messages goes here
        # For example, you can send a welcome message
        welcome_message = {
            "type": "chat.message",
            "data": json.dumps({"message": f"Welcome to the chat"}),
        }
        await self.chat_message(welcome_message)

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
