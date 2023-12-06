from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connected...")
        print(f"event = {event}")

        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        print(f"message received from client = {event['text']}")

        self.send(
            {"type": "websocket.send", "text": "Hello, I am Django's sync consumer"}
        )

    def websocket_disconnect(self, event):
        print("Websocket, Disconnect...")
        print(f"event = {event}")
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket Connected...")

        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print(f"message received from client = {event['text']}")

        await self.send(
            {"type": "websocket.send", "text": "Hello,  I am Django's async consumer"}
        )

    async def websocket_disconnect(self, event):
        print("Websocket, Disconnect...")
        print(f"event = {event}")
        raise StopConsumer()
