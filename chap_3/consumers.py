from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connected...")
        print(f"event = {event}")

        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        print(f"message received from client = {event['text']}")

        for i in range(30):
            self.send(
                {
                    "type": "websocket.send",
                    "text": f"Hello, I am Django's sync consumer = {i +1}",
                }
            )

            sleep(1)

    def websocket_disconnect(self, event):
        print("Websocket, Disconnect...")
        print(f"event = {event}")
        raise StopConsumer()


import asyncio

import json


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket Connected...")

        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print(f"message received from client = {event['text']}")
        # for i in range(20):
        #     await self.send(
        #         {
        #             "type": "websocket.send",
        #             "text": f"Hello,  I am Django's async consumer from chap_3= {i+1}",
        #         }
        #     )
        #     await asyncio.sleep(1)

        message = {
            "logo": "	https://schoolies-spaces.sgp1.digitaloceanspaces.com/static/images/logo_name_header.svg",
            "text": "Schoolies",
        }

        await self.send({"type": "websocket.send", "text": json.dumps(message)})

    async def websocket_disconnect(self, event):
        print("Websocket, Disconnect...")
        print(f"event = {event}")
        raise StopConsumer()
